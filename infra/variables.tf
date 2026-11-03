variable "aws_region" {
  description = "AWS region to deploy the orchestrator infrastructure into."
  type        = string
  default     = "eu-central-1"
}

variable "aws_profile" {
  description = <<-EOT
    Local AWS CLI profile to use for authentication. No default on purpose --
    keeps account-targeting explicit rather than silently baked in. Must
    point at a profile authenticated against account 830495964081 (DAI-CST),
    e.g. set up via `aws configure sso` before the first `terraform apply`.
  EOT
  type        = string
}

variable "github_app_id" {
  description = <<-EOT
    GitHub App ID. The App itself cannot be created via Terraform (no
    provider supports it) -- a human creates it via GitHub's web UI
    (Settings -> Developer settings -> GitHub Apps -> New GitHub App) with
    `pull_requests: write`, `issues: write`, `actions: write` permissions
    (no admin), installs it on senacor3/software-factory-demo, and supplies
    this value.
  EOT
  type        = string
}

variable "github_app_installation_id" {
  description = "Installation ID of the GitHub App on senacor3/software-factory-demo (human-supplied, from the App's install step)."
  type        = string
}

variable "github_app_private_key_pem" {
  description = <<-EOT
    PEM-encoded private key downloaded for the GitHub App. Never committed
    and has no default -- supply only via `-var`, a `.tfvars` file excluded
    from git, or a `TF_VAR_github_app_private_key_pem` env var at apply
    time. Stored in Secrets Manager, never baked into the Lambda package.
  EOT
  type        = string
  sensitive   = true
}
