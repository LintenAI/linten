output "lb_ip" {
  description = "Global anycast IP of the external load balancer."
  value       = module.linten.lb_ip
}

output "lb_url" {
  description = "Proxy URL. Dashboard at /, API at /v1/*."
  value       = module.linten.lb_url
}

output "gateway_service_url" {
  description = "Default Cloud Run URL for the gateway (bypasses the LB)."
  value       = module.linten.gateway_service_url
}

output "backend_service_url" {
  description = "Default Cloud Run URL for the backend (bypasses the LB)."
  value       = module.linten.backend_service_url
}

output "ui_service_url" {
  description = "Default Cloud Run URL for the UI (bypasses the LB)."
  value       = module.linten.ui_service_url
}

output "cloudsql_writer_ip" {
  description = "Private IP of the Cloud SQL writer."
  value       = module.linten.cloudsql_writer_ip
}

output "cloudsql_reader_ip" {
  description = "Private IP of the Cloud SQL read replica."
  value       = module.linten.cloudsql_reader_ip
}

output "redis_endpoint" {
  description = "Memorystore Redis endpoint."
  value       = module.linten.redis_endpoint
}

output "redis_host" {
  description = "Memorystore Redis host."
  value       = module.linten.redis_host
}

output "redis_port" {
  description = "Memorystore Redis port."
  value       = module.linten.redis_port
}

output "redis_server_ca_pem" {
  description = "Memorystore server CA PEM."
  value       = module.linten.redis_server_ca_pem
}

output "db_username" {
  description = "Cloud SQL application username."
  value       = module.linten.db_username
}

output "db_name" {
  description = "Cloud SQL database name."
  value       = module.linten.db_name
}

output "gcs_bucket" {
  description = "GCS bucket name."
  value       = module.linten.gcs_bucket
}

output "master_key_secret_id" {
  description = "Secret Manager resource ID holding LINTEN_MASTER_KEY."
  value       = module.linten.master_key_secret_id
}

output "db_password_secret_id" {
  description = "Secret Manager resource ID holding the Cloud SQL app-user password."
  value       = module.linten.db_password_secret_id
}

output "runtime_service_account_email" {
  description = "Runtime service account email."
  value       = module.linten.runtime_service_account_email
}

output "migration_run_command" {
  description = "Break-glass command to re-run the one-off migration job."
  value       = module.linten.migration_run_command
}
