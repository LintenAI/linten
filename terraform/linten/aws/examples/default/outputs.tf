output "alb_dns_name" {
  description = "Public DNS name of the Linten ALB."
  value       = module.linten.alb_dns_name
}

output "alb_url" {
  description = "Proxy URL. Dashboard at /, API at /v1/*."
  value       = module.linten.alb_url
}

output "ecs_cluster" {
  description = "ECS cluster name."
  value       = module.linten.ecs_cluster
}

output "vpc_id" {
  description = "VPC the stack runs in, whether module-created or supplied."
  value       = module.linten.vpc_id
}

output "task_security_group_id" {
  description = "Tasks security group. Allow this inbound on an existing database or Redis."
  value       = module.linten.task_security_group_id
}

output "aurora_writer_endpoint" {
  description = "Aurora writer endpoint."
  value       = module.linten.aurora_writer_endpoint
}

output "aurora_reader_endpoint" {
  description = "Aurora reader endpoint."
  value       = module.linten.aurora_reader_endpoint
}

output "redis_endpoint" {
  description = "ElastiCache Redis primary endpoint (TLS)."
  value       = module.linten.redis_endpoint
}

output "s3_bucket" {
  description = "S3 bucket name."
  value       = module.linten.s3_bucket
}

output "master_key_secret_arn" {
  description = "Secrets Manager ARN holding LINTEN_MASTER_KEY."
  value       = module.linten.master_key_secret_arn
}

output "db_master_password_secret_arn" {
  description = "Secrets Manager ARN holding the Aurora master credentials (bootstrap-only)."
  value       = module.linten.db_master_password_secret_arn
}

output "db_bootstrap_sql" {
  description = "Run once as the master DB user to create the IAM-authed app user."
  value       = module.linten.db_bootstrap_sql
}

output "migration_run_command" {
  description = "Break-glass command to re-run the one-off prisma migration task."
  value       = module.linten.migration_run_command
}
