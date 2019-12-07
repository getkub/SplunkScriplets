* Following 4V's of Big Data **Volume**, **Variety**, **Velocity**, **Veracity # Uncertainity**

## Preparation

* Identify and research about sourcetype and data
* Check for pre-existing Splunk supported Technology Add-on
* Desired output from end-users
* How much data would be coming? How it will come Streaming/Forwarder/syslog etc
* Naming standards for objects. 
* Integration required (like AD)
* Deployment server and clustering considerations

## Index-time & Search-time Consideration

* Timestamp,sourcetype,line-breaks etc
* Transforms required? (eg Credit card masking)
* Field mapping
* Check if the knowledge objects already done (Knowledge endpoint descriptions)
* Stick to CIM mapping
* Data model creation (customised)

## Platform scalability and deployment
* Extra Splunk infrastructure required?
* License considerations
* Validating connectivity, firewall, Disaster recovery
* Users, roles, AD integration

## Validation
* Event breaking, timestamp, host, source and sourcetype
* Data Model, tags, eventtypes
* User Permission/roles
