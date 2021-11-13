module "mod-network-test" {
    source = "../generic_mods/network"
    project_id = var.project_id
    default_region = var.default_region
    network_name = var.network_name
    subnets_obj = var.subnets_obj
}

module "mod-firewall-test" {
    depends_on = [module.mod-network-test]
    source = "../generic_mods/firewall"
    project_id = var.project_id
    default_region = var.default_region
    network_name = var.network_name
    fw_obj = var.fw_obj
}

module "mod-app-static-ip" {
    source = "../generic_mods/static_ip"
    project_id = var.project_id
    default_region = var.default_region
    app_static_ip_obj = var.app_static_ip_obj
}

resource "random_id" "db_name_suffix" {
    byte_length = 4
}

module "mod-sql-test-postgress" {
    source = "../generic_mods/sql_postgress"
    project_id = var.project_id
    default_region = var.default_region
    network_name = module.mod-network-test.network_name
    database_obj = var.database_obj
}
