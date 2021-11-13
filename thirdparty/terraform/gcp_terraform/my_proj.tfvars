network_name = "my-vpc-01"
subnets_obj = {
    "my-subnet-01" = {
        "subnet_ip_cidr" = "10.10.0.0/16"
        "subnet_ip_range_services_cidr": "10.11.0.0/16"
        "subnet_ip_range_pods_cidr": "10.12.0.0/16"
    },
}

db_obj = {
    "my-sql-instan" = {
        "tier" = "db-g1-small"
        "database_version" = "POSTGRES_13" 
        "disk_size" = "100"
        "retained_backups" = "10"
        "transaction_log_retention_days" = "7"
        "db_user" = "myuser"
        "db_password" = "mycomplexpass"
    },
}

app_static_ip_obj = {
    "my-1stapp-static-ip" = {
        "default_region" = "europe-west2"
    },
    "my-2ndapp-static-ip" = {
        "default_region" = "europe-west2"
    },
}

# Ensure tags follow GCP standards Must be a match of regex '(?:[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?)
fw_obj = {
    "my-fw-tcp-22" = {
        "description" = "Allow SSH 22"
        "direction": "INGRESS"
        "action" = "allow"
        "protocol" = "tcp"
        "ports": ["22"]
        "destination_ranges": []
        "source_tags": []
        "source_ranges" = ["1.1.1.1/32"]
        "target_tags": ["ssh"]
        "priority": 1000
    },
}

# ================================#
# GKE cluster settings
# ================================#

gke_cluster_name = "my-cluster"
