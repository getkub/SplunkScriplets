# SplunkScriplets
### Various Splunk related scripts, tricks and notes .. All in ONE Place

# Directory Structure
```
├── devOps
│   ├── SplunkEnterprise
│   │   └── archive
│   └── SplunkUF
│       └── SPF_Install
├── docs
│   └── splunk_tips
│       ├── answers
│       ├── api
│       ├── apps
│       │   └── A_prod_ldap_auth
│       │       └── local
│       ├── configs
│       │   └── sample_app
│       │       └── local
│       ├── dashboards
│       │   └── dashboard_samples
│       ├── others
│       │   ├── errors
│       │   │   └── memoryLeak
│       │   └── notes
│       └── searches
├── sampleData
└── thirdparty
    ├── ansible
    │   ├── basic
    │   │   ├── configs
    │   │   ├── group_vars
    │   │   ├── roles
    │   │   │   ├── distributor_role
    │   │   │   │   └── tasks
    │   │   │   ├── git
    │   │   │   │   └── tasks
    │   │   │   └── github
    │   │   │       └── tasks
    │   │   ├── templates
    │   │   └── vault
    │   ├── hortonew
    │   │   ├── group_vars
    │   │   ├── playbooks
    │   │   └── roles
    │   │       ├── universal_forwarder_linux
    │   │       │   └── tasks
    │   │       └── universal_forwarder_windows
    │   │           ├── files
    │   │           └── tasks
    │   └── splunk_apps
    ├── arcsight
    ├── certs
    ├── curl
    ├── dataCapture
    ├── disk
    ├── docker
    ├── encode_decode
    ├── eventgen
    ├── git
    ├── gitlab
    ├── k8s_kubernetes
    ├── kafka
    ├── linux
    ├── logrotate
    ├── mouse
    ├── network
    │   └── scapy
    ├── openldap
    ├── openssl
    ├── pandoc
    ├── perl
    ├── powershell
    │   └── user_bulk
    ├── preChecks
    ├── python
    │   └── scapy
    ├── quest
    ├── regexes
    ├── rsyslog
    ├── ruby
    ├── shell
    ├── snmp
    ├── soc_usecases
    ├── standards
    │   ├── ISO
    │   │   └── iso27001
    │   └── pci
    ├── vagrant
    └── virtualbox

```
## What does each Directory include
- devOps => Splunk and Universal Forwarder installation Scripts
- thirdPary => ThirdParty Scripts like python, shell scripts, connectivity tests etc.
- splunk_tips => UI development snippets, Tricky searches which can be re-used, Any rare errors which people have noted and workarounds, Some key configs like rsyslogd, serverclass.conf, authentication.conf etc.

## TO DO
- Create a good repository to put notes related to Splunk and its automation
