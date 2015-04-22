####### --------------------------------------------------
### Instructions - Splunk DevOps Management
####### --------------------------------------------------
##### Summary of Devops Activities
 - Install Splunk Enterprise
 - Install Splunk Forwarders
 - Generate code for Splunk-apps automatically for environment
 - Deploy Splunk-apps for environment

#######--------------------------------------------------
##### Pre-reqs for installation
#######--------------------------------------------------
 - root access
 - SVN or source-code repo
 - Splunk Enterprise installable
 - Splunk Forwarder installable
 - Port connectivity (see below)
 - code templating tools (Sample uses pystache with {{variable}} notation )

#######--------------------------------------------------
#####  Splunk Ports requirement
#######--------------------------------------------------
######  Splunk Enterprise Ports requirement

- 8000: Splunk WebPort
- 8089: Splunk management Port
- 514 : TCP : If using syslog or tcp Input
- 8065: AppServer Port
- 9997: Splunk forwarder Indexer port 
- 8191: Splunk CRUD activities for KV Store # Nice to have

######  Splunk Forwarder Ports requirement
- 8089: Splunk Forwarder management Port

######  Splunk Forwarder <-> Splunk Enterprise
- Splunk Enterprise should be able to connect to 8089 of Forwarders
- Splunk Forwarder should be able to connect to 8089 and 9997 of masters

#######--------------------------------------------------
#####  Splunk Enterprise Install
#######--------------------------------------------------
Installation consists of ** (1) Infrastructure (2) Apps **
#####  Infrastructure
- ```./splunkEnterpriseInstall.sh```  # *(as root)*
- Splunk auto-boot *(init.d)* files will be also copied 
- Splunk upgrade also in-built with this

#####  Apps
- ``` python codeGenerator.py sourceDir configFile environment ```
- eg: 
` 
python codeGenerator.py /DATA/devops/svn/splunkForwader/ /DATA/devops/svn/configs/splunk.apps.config PROD
` 
- apps will be created in `/tmp/workspace.YYYYmmddHHMMSS` directory
- Replace the apps in `$SPLUNK_HOME/etc/apps/` by above
- SPLUNK & DevOps Team should manage contents in `svn` directory

#######--------------------------------------------------
#####  Splunk Forwarder Install
#######--------------------------------------------------
#####  Infrastructure
- Edit deployment Server within the script (or automate it)
- ```./splunkForwarderInstall.sh```  # *(as root)*
- Splunk auto-boot *(init.d)* files will be also copied 

#####  Apps
- Apps would be automatically deployed from parent deployment Server


#######--------------------------------------------------
#####  End of Document
#######--------------------------------------------------
