## Opentelemetry Metric Data Types (Signals)

Here's a table summarizing the different data types used for metrics in Opentelemetry and their typical use cases:

| Data Type | Description | Use Case | Example |
|---|---|---|---|
| Histogram | Captures the distribution of values over time. | Metrics that vary significantly | Response times, API call durations |
| Counter | Represents a continuously increasing count of events. | Total number of occurrences | Odometer of Car which always goes up |
| Gauge | Represents the current value of a metric at a specific point in time. | Metrics that can fluctuate | System memory usage, number of active users,  Gauges are asynchronous |
| Sum | Continuously increasing sum (can be reset). | Accumulated values over time | Total bytes transferred (with periodic resets) |
| Summary (Legacy) | Combines counter and histogram aspects. | Less common use cases (consider alternatives) |  |
