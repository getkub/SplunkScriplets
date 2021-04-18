| Ability | estreamer | syslog | Better Option? |
| ------------- | ------------- | ------------- | ------------- |
| Data transfer Method | estreamer addon pulls data | Data is pushed to syslog server | syslog |
| Splunk tier/hardware requirements | heavy forwarder or collection layer requried | Can use existing syslog location | syslog |
| Data quality | Multiple datasets can be fetched | Limited datasets only | estreamer |
| Commercial Support | estreamer is NOT splunk official addon. So support has to be handled by Splunk admin or officially bought from Cisco TAC | Data is pushed, so no real issues | syslog |
| Splunk Upgrade comptability | At mercy of estreamer developer or on admin | No such issues | syslog |
| CIM and datamodels | Plenty of security data. Malware, authentication, User activity, Intrusion etc available | Minimal data for auditing, authentication | estreamer |
| Collection interval | Since it is polling, it is done in intervals. | Real-time data | syslog |
| Complexity of Implementation | Few installations and configurations required. Separate python/perl required. | Minimal installation as it is just collection | syslog |
| Certificates | Separate certificates needs to be generated & maintained and co-ordinated with your Network support team. This needs to be loaded alongside | Use the existing colleciton mechanism | syslog |
| Additional OS modules & footprint | Old estreamer required perl modules. New one may require seperate python installation (Not 100% sure) | No separate modules required | syslog |
| Data volume & splunk license | Extended data and sourcetypes | Less data due to minimal dataset | NA |
