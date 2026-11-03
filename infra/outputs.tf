output "function_url" {
  description = "Public URL for invoking the orchestrator Lambda via its Function URL."
  value       = aws_lambda_function_url.orchestrator.function_url
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table holding orchestrator control-plane state."
  value       = aws_dynamodb_table.orchestrator_state.name
}
