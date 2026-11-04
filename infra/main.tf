terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

data "aws_caller_identity" "current" {}

locals {
  build_dir     = "${path.module}/build"
  function_name = "light-factory-orchestrator"
  table_name    = "light-factory-orchestrator-state"
  # Must match `_GITHUB_APP_SECRET_NAME` in orchestrator/handler.py -- the
  # Lambda's IAM role is scoped to read only this one secret's ARN (AD-18).
  github_app_secret_name = "light-factory-orchestrator-github-app"
}

# Packaging: install the (currently empty) requirements.txt pins alongside
# handler.py into a build directory, then zip it. Reproducible from
# orchestrator/ on every apply -- never a deliverable itself.
resource "null_resource" "install_dependencies" {
  triggers = {
    requirements_hash     = filesha256("${path.module}/../orchestrator/requirements.txt")
    handler_hash          = filesha256("${path.module}/../orchestrator/handler.py")
    github_app_hash       = filesha256("${path.module}/../orchestrator/github_app.py")
    auth_hash             = filesha256("${path.module}/../orchestrator/auth.py")
    comment_commands_hash = filesha256("${path.module}/../orchestrator/comment_commands.py")
    dynamodb_state_hash   = filesha256("${path.module}/../orchestrator/dynamodb_state.py")
  }

  provisioner "local-exec" {
    command = <<-EOT
      rm -rf "${local.build_dir}"
      mkdir -p "${local.build_dir}"
      cp "${path.module}/../orchestrator/handler.py" "${local.build_dir}/"
      cp "${path.module}/../orchestrator/github_app.py" "${local.build_dir}/"
      cp "${path.module}/../orchestrator/auth.py" "${local.build_dir}/"
      cp "${path.module}/../orchestrator/comment_commands.py" "${local.build_dir}/"
      cp "${path.module}/../orchestrator/dynamodb_state.py" "${local.build_dir}/"
      pip install --quiet -r "${path.module}/../orchestrator/requirements.txt" -t "${local.build_dir}" \
        --platform manylinux2014_x86_64 --implementation cp --python-version 3.13 --only-binary=:all:
    EOT
  }
}

data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = local.build_dir
  output_path = "${path.module}/lambda_package.zip"

  depends_on = [null_resource.install_dependencies]
}

resource "aws_iam_role" "lambda_exec" {
  name = "${local.function_name}-lambda-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

# Least-privilege: this Lambda's own log group only.
resource "aws_iam_role_policy" "lambda_logs" {
  name = "lambda-logs"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
      ]
      Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${local.function_name}:*"
    }]
  })
}

# Least-privilege: this Lambda's own table access only, no attributes beyond
# the partition key (control-plane state only, never git-committed content).
resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "lambda-dynamodb"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
      ]
      Resource = aws_dynamodb_table.orchestrator_state.arn
    }]
  })
}

# Fine-grained GitHub PAT (AD-18), plus the webhook and stage-callback
# shared secrets (story 3): human creates the PAT via GitHub's web UI (no
# Terraform provider can create it), then supplies it, and separately
# chooses the two caller-auth shared secrets, as the three sensitive
# variables below. One secret, one JSON blob -- never hardcoded, never
# committed. A second secret for webhook_secret/stage_callback_secret was
# considered and rejected (see story 3's Design Notes): it would double
# the `get_secret_value` call on every request, and the existing IAM
# policy is already scoped to exactly this one ARN.
resource "aws_secretsmanager_secret" "github_app" {
  name = local.github_app_secret_name

  # No data-loss risk from skipping AWS's default 30-day soft-delete
  # window -- the secret's content is always re-suppliable from the same
  # GitHub PAT and shared secrets. Without this, a destroy+re-apply cycle during
  # local iteration would fail trying to recreate a secret with the same
  # name until that window elapsed.
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "github_app" {
  secret_id = aws_secretsmanager_secret.github_app.id
  secret_string = jsonencode({
    github_pat            = var.github_pat
    webhook_secret        = var.github_webhook_secret
    stage_callback_secret = var.stage_callback_secret
  })
}

# Least-privilege: this Lambda's role can read only this one secret's ARN,
# never any other secret in the account (AD-18).
resource "aws_iam_role_policy" "lambda_github_app_secret" {
  name = "lambda-github-app-secret"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["secretsmanager:GetSecretValue"]
      Resource = aws_secretsmanager_secret.github_app.arn
    }]
  })
}

resource "aws_lambda_function" "orchestrator" {
  function_name = local.function_name
  role          = aws_iam_role.lambda_exec.arn

  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256

  handler = "handler.handler"
  runtime = "python3.13"
  timeout = 10
}

resource "aws_lambda_function_url" "orchestrator" {
  function_name      = aws_lambda_function.orchestrator.function_name
  authorization_type = "NONE"
}

# Required for authorization_type = "NONE" to actually permit invocation --
# the Function URL's own auth setting is necessary but not sufficient; the
# function's resource policy must separately allow it.
resource "aws_lambda_permission" "function_url_public" {
  statement_id           = "AllowPublicInvokeFunctionUrl"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.orchestrator.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

# Control-plane state only, keyed on the composite partition key. No
# attributes beyond the hash key per this story's boundaries.
resource "aws_dynamodb_table" "orchestrator_state" {
  name         = local.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "story_slug#run_id"

  attribute {
    name = "story_slug#run_id"
    type = "S"
  }
}
