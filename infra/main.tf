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
}

# Packaging: install the (currently empty) requirements.txt pins alongside
# handler.py into a build directory, then zip it. Reproducible from
# orchestrator/ on every apply -- never a deliverable itself.
resource "null_resource" "install_dependencies" {
  triggers = {
    requirements_hash = filesha256("${path.module}/../orchestrator/requirements.txt")
    handler_hash      = filesha256("${path.module}/../orchestrator/handler.py")
  }

  provisioner "local-exec" {
    command = <<-EOT
      rm -rf "${local.build_dir}"
      mkdir -p "${local.build_dir}"
      cp "${path.module}/../orchestrator/handler.py" "${local.build_dir}/"
      pip install --quiet -r "${path.module}/../orchestrator/requirements.txt" -t "${local.build_dir}"
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
