## Useful Links

- https://www.elastic.co/guide/en/observability/current/apm-distributed-tracing.html
- https://opentelemetry.io/docs/specs/otel/metrics/data-model/
- https://opentelemetry.io/docs/collector/
- https://grafana.com/blog/2024/04/18/a-guide-to-scaling-opentelemetry-collectors-across-multiple-hosts-via-ansible/
- https://opentelemetry.io/docs/specs/semconv/resource/host/
- https://opentelemetry.io/docs/collector/quick-start/

### Good Designs
- https://www.elastic.co/blog/native-opentelemetry-support-in-elastic-observability
- https://github.com/elastic/observability-examples/tree/main/Elastiflix
- https://opentelemetry.io/docs/demo/architecture/

- OpenTelemetry Custom Extensions (https://www.youtube.com/watch?v=hXTlV_RnELc)
- Actual implementation: https://www.youtube.com/watch?v=H9bAMRmaaxk

### Distibuted Tracing Summary

 - A trace is a group of transactions and spans with a common root. Each trace tracks the entirety of a single request. When a trace travels through multiple services, as is common in a microservice architecture, it is known as a distributed trace.

- Distributed tracing enables you to analyze performance throughout your microservice architecture by tracing the entirety of a request — from the initial web request on your front-end service all the way to database queries made on your back-end services.


