### forwarder related Examples

```
# To check forwarder sending data 
index=_internal host=*fwd* source=*metrics.log group=syslog* | timechart span=1m sum(tcp_KBps) by host
index=_internal host=*fwd* source=*metrics.log group=thruput | timechart span=1m sum(kb) by host
```
