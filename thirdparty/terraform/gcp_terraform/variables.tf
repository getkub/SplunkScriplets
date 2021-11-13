variable "project_id" {
  description = "The project ID to host the network in"
}

variable "env_tag" {
  description = "env_tag"
}

variable "network_name" {
  description = "network_name"
}

variable "default_region" {
  description = "default_region"
}

variable "default_zone" {
  description = "default_zone"
}

variable "gcp_zones" {
  description = "gcp_zones"
}

variable "subnets_obj" {
  description = "Subnets in MAP format"
}

variable "fw_obj" {
  description = "Firewalls in MAP format"
}

variable "db_obj" {
  description = "Database in MAP format"
}

variable "app_static_ip_obj" {
  description = "static in MAP format"
}

