# SplunkScriplets
### Various Splunk related configs, support items, tricks and notes .. All in ONE Place
The repository is NOT just for Splunk itself, must mostly collection of third party surroundings (like OS, firewalls) and snippets which are useful for an enterprise grade Splunk deployment

# Directory Structure
```
.
├── devOps
│   ├── SplunkEnterprise
│   │   └── archive
│   ├── SplunkUF
│   │   └── SPF_Install
│   └── api_integration
│       └── ansible
│           ├── apps
│           │   └── mysearch
│           │       └── local
│           └── lib
├── docs
│   └── splunk_tips
│       ├── answers
│       ├── api
│       ├── apps
│       │   └── A_prod_ldap_auth
│       │       └── local
│       ├── configs
│       │   └── sample_app
│       │       └── local
│       ├── dashboards
│       │   └── dashboard_samples
│       ├── others
│       │   ├── errors
│       │   │   └── memoryLeak
│       │   └── notes
│       ├── searches
│       └── stanza
├── sampleData
└── thirdparty
    ├── ansible
    │   ├── basic
    │   │   ├── configs
    │   │   ├── group_vars
    │   │   ├── roles
    │   │   │   ├── distributor_role
    │   │   │   │   └── tasks
    │   │   │   ├── git
    │   │   │   │   └── tasks
    │   │   │   └── github
    │   │   │       └── tasks
    │   │   ├── templates
    │   │   └── vault
    │   ├── hortonew
    │   │   ├── group_vars
    │   │   ├── playbooks
    │   │   └── roles
    │   │       ├── universal_forwarder_linux
    │   │       │   └── tasks
    │   │       └── universal_forwarder_windows
    │   │           ├── files
    │   │           └── tasks
    │   └── splunk_apps
    ├── applescript
    │   └── mouse
    ├── arcsight
    ├── certs
    ├── curl
    ├── dataCapture
    ├── disk
    ├── docker
    ├── encode_decode
    ├── esxi
    ├── eventgen
    ├── gcp
    ├── git
    ├── gitlab
    ├── k8s_kubernetes
    ├── kafka
    ├── linux
    ├── logrotate
    ├── mouse
    ├── network
    ├── nginx
    ├── nodejs
    │   └── dropdown
    ├── openldap
    ├── openssl
    ├── pandoc
    ├── perl
    ├── php
    │   └── shellScriptTrigger
    ├── powershell
    │   └── user_bulk
    ├── preChecks
    ├── python
    ├── quest
    ├── regexes
    ├── rsyslog
    ├── ruby
    ├── scapy
    ├── shell
    ├── snmp
    ├── soc_usecases
    ├── standards
    │   ├── ISO
    │   │   └── iso27001
    │   └── pci
    ├── terraform
    │   └── terraformer
    ├── vagrant
    └── virtualbox

```
## What does each Directory include
- devOps => Splunk and Universal Forwarder installation Scripts
- thirdPary => ThirdParty Scripts like python, shell scripts, connectivity tests etc.
- splunk_tips => UI development snippets, Tricky searches which can be re-used, Any rare errors which people have noted and workarounds, Some key configs like rsyslogd, serverclass.conf, authentication.conf etc.

## TO DO
- Create a good repository to put notes related to Splunk and its automation
