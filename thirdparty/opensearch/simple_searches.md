## Workbench tool
```
search source=opensearch_dashboards_sample_data_ecommerce | dedup total_unique_products

search source=opensearch_dashboards_sample_data_ecommerce | fields customer_gender,category | stats count() as count by customer_gender,category| fields customer_gender,category,count
```
