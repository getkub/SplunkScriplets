### Passing required resources

```
projects="my-project"
regions="europe-west2"
resources_all="addresses,autoscalers,backendBuckets,backendServices,bigQuery,cloudFunctions,cloudsql,dataProc,disks,externalVpnGateways,dns,firewall,forwardingRules,gcs,gke,globalAddresses,globalForwardingRules,healthChecks,httpHealthChecks,httpsHealthChecks,iam,images,instanceGroupManagers,instanceGroups,instanceTemplates,instances,interconnectedAttachments,kms,logging,memoryStore,monitoring,networks,packetMirrorings,nodeGroups,nodeTemplates,project,pubsub,regionAutoscalers,regionBackendServices,regionDisks,regionHealthChecks,regionInstanceGroups,regionSslCertificates,regionTargetHttpProxies,regionTargetHttpsProxies,regionUrlMaps,reservations,resourcePolicies,regionInstanceGroupManagers,routers,routes,schedulerJobs,securityPolicies,sslCertificates,sslPolicies,subnetworks,targetHttpProxies,targetHttpsProxies,targetInstances, targetPools,targetSslProxies,targetTcpProxies,targetVpnGateways,urlMaps,vpnTunnels"
resources_basic="addresses,autoscalers,cloudFunctions,disks,externalVpnGateways,dns,firewall,forwardingRules,gcs,gke,globalAddresses,globalForwardingRules,iam,images,instanceGroupManagers,instanceGroups,instanceTemplates,instances,kms,logging,memoryStore,monitoring,networks,packetMirrorings,nodeGroups,nodeTemplates,project,pubsub,regionAutoscalers,regionBackendServices,regionDisks,regionHealthChecks,regionInstanceGroups,regionSslCertificates,regionTargetHttpProxies,regionTargetHttpsProxies,regionUrlMaps,reservations,resourcePolicies,regionInstanceGroupManagers,routers,routes,schedulerJobs,securityPolicies,sslCertificates,sslPolicies,subnetworks,targetHttpProxies,targetHttpsProxies,targetInstances, targetPools,targetSslProxies,targetTcpProxies,targetVpnGateways,urlMaps,vpnTunnels"

# eg: terraformer import google --projects=${projects} --regions=${regions} --resources=routes

terraformer import google --projects=${projects} --regions=${regions} --resources=${resources_basic}
```
