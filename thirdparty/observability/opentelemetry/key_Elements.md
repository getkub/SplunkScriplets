
## Key Elements for Traces, Metrics, and Logs in Opentelemetry
- Showing if the element is 'mandatory' in each core data-types

| Element | Description | Traces | Metrics |  Logs |
|---|---|---|---|---|
| traceId | Unique identifier for the trace | Yes | No | No |
| spans | Array of units of work within the trace | Yes | No | No |
| name | Descriptive name for the span/metric | Recommended | Yes | No |
| kind | Role of the span (CLIENT, SERVER, etc.) | Recommended | No | No |
| attributes | Key-value pairs with details | Optional | Optional | Optional |
| startTime | Timestamp when the span/metric started | Mandatory | Optional (recommended) | Mandatory |
| endTime | Timestamp when the span ended | Mandatory | No | No |
| parentSpanId | Links a span to its parent within the trace | Optional | No | No |
| type | Data type of the metric value (Gauge, Counter) | No | Yes | No |
| value | Numerical value of the metric | No | Yes | No |
| severity | Level of the log message (DEBUG, INFO, WARN) | Optional (recommended) | No | Optional (recommended) |
| log message | Text content of the log message | Mandatory | No | Mandatory |
