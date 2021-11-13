resource "google_compute_global_address" "private_ip_address" {
    provider        = google-beta

    project         = var.project_id 
    name            = "sql-postgress-private-ip-address"
    purpose         = "VPC_PEERING"
    address_type    = "INTERNAL"
    prefix_length   = 16
    network         = "${var.network_name.self_link}"
}

resource "google_service_networking_connection" "private_vpc_connection" {
    provider        = google-beta

    network         = "${var.network_name.self_link}"
    service         = "servicenetworking.googleapis.com"
    reserved_peering_ranges = ["${google_compute_global_address.private_ip_address.name}"]
}

resource "random_id" "db_name_suffix" {
  byte_length = 4
}
 
resource "google_sql_database_instance" "instance" {
    provider            = google-beta
    project             = var.project_id
    count               = length(var.db_obj)
    name                = join("-", [element(keys(var.db_obj), count.index), random_id.db_name_suffix.hex])
    database_version    = var.db_obj[element(keys(var.db_obj), count.index)]["database_version"]
    region              = var.default_region
    deletion_protection = false
    depends_on = [
            google_service_networking_connection.private_vpc_connection
        ]
    #encryption_key_name = "projects/my_encrypt_project/locations/europe-west2/keyRings/my-keyring/cryptoKeys/specific-key-gce"

    settings {
        tier                = var.db_obj[element(keys(var.db_obj), count.index)]["tier"]
        availability_type   = "REGIONAL"
        activation_policy   = "ALWAYS"
        disk_size           = var.db_obj[element(keys(var.db_obj), count.index)]["disk_size"]
        disk_autoresize     = "true"
        disk_type           = "PD_SSD" 

        backup_configuration {
            backup_retention_settings {
                retained_backups = var.db_obj[element(keys(var.db_obj), count.index)]["retained_backups"]
                retention_unit   = "COUNT"
            }
            binary_log_enabled             = "false"
            enabled                        = "true"
            location                       = "eu"
            point_in_time_recovery_enabled = "true"
            start_time                     = "02:00"
            transaction_log_retention_days = var.db_obj[element(keys(var.db_obj), count.index)]["transaction_log_retention_days"]
        }
        ip_configuration {
            ipv4_enabled    = false
            private_network = var.network_name.self_link
            require_ssl     = true 
        }
    }
    lifecycle {
        prevent_destroy = true
    }
}

resource "google_sql_database" "my_specific_db" {
    project       = var.project_id
    count         = length(var.db_obj)
    name          = "my_specific_db_prod"
    instance      = google_sql_database_instance.instance[count.index].name
    collation     = "en_US.UTF8"
    charset       = "UTF8"
}

resource "google_sql_user" "dbusers" {
    project         = var.project_id
    count           = length(var.db_obj)
    name            = var.db_obj[element(keys(var.db_obj), count.index)]["db_user"]
    instance        = google_sql_database_instance.instance[count.index].name
    password        = var.db_obj[element(keys(var.db_obj), count.index)]["db_password"]
    deletion_policy = "ABANDON"
}
