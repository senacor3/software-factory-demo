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
