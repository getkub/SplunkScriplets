variable "project_id" {
    description = "project name"
}

variable "default_region" {
    description = "the default region of the sql instance"
}

variable "network_name" {
    description = "name of the network"
}

variable "db_obj" {
    type = map
}
