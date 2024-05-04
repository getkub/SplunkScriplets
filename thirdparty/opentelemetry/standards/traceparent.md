## Traceparent

Distributed tracing relies on injecting a custom traceparent HTTP header into outgoing requests to track the flow of a single request across multiple microservices in a distributed system.

- The traceparent header follows a specific format defined by the W3C Trace Context specification:
```
version-trace_id-parent_id-trace_flags
```

eg : Through Service A, B & C, it has below headers
```
traceparent at Service A: 00-trace_id_A-00-01
traceparent at Service B: 00-trace_id_B-trace_id_A-01
traceparent at Service C: 00-trace_id_C-trace_id_A-01
```