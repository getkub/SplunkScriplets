## Sample detection repo structure

```
detections-repo/
│
├── static/                             # Folder for static use cases (hardcoded YAML)
│   ├── UC_S_0001.yml                   # Static use case 1 (hardcoded YAML file)
│   ├── UC_S_0002.yml                   # Static use case 2 (hardcoded YAML file)
│   └── UC_S_0003.yml                   # Static use case 3 (hardcoded YAML file)
│
├── dynamic/                            # Folder for dynamic use cases (Ansible Jinja2 templates)
│   ├── UC_D_0001.yml.j2                # Dynamic use case 1 (Jinja2 template)
│   ├── UC_D_0002.yml.j2                # Dynamic use case 2 (Jinja2 template)
│   └── UC_D_0003.yml.j2                # Dynamic use case 3 (Jinja2 template)
│
├── vendor/                             # Folder for vendor use cases
│   ├── UC_V_0001.yml                   # Vendor use case 1 (static YAML file)
│   ├── UC_V_0002.yml                   # Vendor use case 2 (static YAML file)
│   └── UC_V_0003.yml                   # Vendor use case 3 (static YAML file)
│
├── mapping/                            # Mapping folder for separate vendor/custom mappings
│   ├── vendor_uc_mapping.csv           # Mapping CSV file for vendor use cases
│   ├── static_uc_mapping.csv           # Mapping CSV file for static use cases
│   ├── dynamic_uc_mapping.csv          # Mapping CSV file for dynamic use cases
│
└── README.md                           # Repo documentation (optional)
```
