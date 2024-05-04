## Interview Questions for Principal Observability Engineer (AWS Focus)

**Observability Concepts and Tools:**

1. **Deep Dive on Metrics:**
* Explain the difference between Cardinality and Dimensionality in metrics. How do you handle high cardinality metrics in an AWS environment?

    - **Cardinality**: Imagine you have a dataset of customer transactions, and one of the dimensions is "Product ID." Each transaction records the product that a customer purchased. Now, if you have a wide range of products in your inventory, each with a unique ID, the cardinality of the "Product ID" dimension would be high. For instance, if you have 10,000 unique products, the cardinality of this dimension would be 10,000.

        Can be reduced by 
        - Sampling
        - aggregating data
        - Hashing

    - **Dimension**: Consider a dataset tracking website traffic. You may have dimensions such as "Date," "Page URL," "Referrer," "Device Type," "Browser," and "Country." Each of these dimensions adds to the overall dimensionality of your dataset. So if you have these six dimensions, your dataset's dimensionality would be 6.

        Can be reduced by 
        - Tags

* Describe different types of aggregations used for metrics (e.g., sum, count, average) and when you would use each.
* How can you leverage Amazon CloudWatch metrics for anomaly detection?
    - Metric Filters and Alarms: Thresholds, trigger alarm & Anomalies
    - Anomaly Detection Model: ML detect anomalies in your metric data
    - CloudWatch Logs Insights: query and analyze log data
    - Integration with AWS Lambda & SNS: Invoke Lambdas or notifications via Amazon SNS

2. **Distributed Tracing Expertise:**
    * Explain the concept of distributed tracing and its benefits for troubleshooting complex microservices architectures.
    * Walk us through the process of implementing distributed tracing with a tool like AWS X-Ray. 
    * How can you use distributed tracing data to identify performance bottlenecks in an application?

3. **OpenTelemetry Knowledge:**
    * Describe your experience with the OpenTelemetry project.
        - OpenTelemetry is an Observability framework and toolkit designed to create and manage telemetry data such as traces, metrics, and logs
        - Contributed to OpenTelemetry Semantic Conventions for Elastic Search Integration: I actively participated in defining and refining OpenTelemetry Semantic Conventions for Elastic Search data. This involved collaborating with the Elastic and OpenTelemetry communities to ensure seamless mapping between Elastic Search field notations and the standardized fields defined by OTEL.
        - OTEL Implementation Discussions: I collaborated with application development teams to discuss the implementation of OTEL standards within their applications. This involved explaining the benefits of OTEL, identifying appropriate instrumentation points, and guiding the team on integrating OTEL libraries for trace and metric collection.
    * Explain the benefits of using OpenTelemetry for instrumenting applications compared to vendor-specific solutions.
        - Vendor Neutrality Reduced Lock-In
        - NOT worrying about compatibility issues
        - Unified APIs for Development team
        - Polyglot Support - libraries for various programming languages
        - Standardized Data makes it easy for End Content team
        - Best observability practices
        - Open Source Advantage


    * How would you approach migrating an existing monitoring setup to use OpenTelemetry with AWS services?
        - Inventory and Evaluation
        - Mapping and Gap Analysis
        - Backend Selection
        - Phased Approach
        - Instrumentation applications with OpenTelemetry
        - Alerting and Notification
        - Training & Support

**AWS Observability and Scalability:**

4. **Building and Running Large-Scale Systems on AWS:**
    * Describe your experience architecting and deploying highly scalable distributed systems on AWS

        ### Data Flow Architecture

        1. **Clients Send Data**: Applications send log and metrics data to the configured endpoint in Route 53.
        2. **Route 53 Directs Traffic**: Route 53 directs traffic to the Application Load Balancer (ALB).
        3. **ALB Distributes Load**: The ALB distributes incoming data requests across healthy Logstash instances in the Auto Scaling Group.
        4. **Logstash Parses and Transforms**: Each Logstash instance parses incoming data, extracting relevant information and potentially enriching it.
        5. **Kafka Queues Data**: Kafka acts as a buffer, decoupling Logstash from Elasticsearch and ensuring data is not lost if individual Elasticsearch nodes fail.


    * How do you leverage AWS services like Auto Scaling Groups and CloudWatch alarms for proactive capacity management?

    * Discuss strategies for optimizing the cost-efficiency of your observability solution on AWS.

5. **Troubleshooting Platforms on AWS:**
    * Describe a situation where you used observability data to identify and resolve a critical production incident on AWS.

**Bonus Questions:**

* Discuss your experience with integrating observability data with other tools like dashboards (e.g., Grafana) or alerting systems (e.g., PagerDuty).
    - 
* How would you approach building a disaster recovery plan for your observability infrastructure on AWS?
* Share your thoughts on emerging trends in observability and how they might impact your approach in the future.
