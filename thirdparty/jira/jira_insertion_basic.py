import requests
from datetime import datetime, timedelta

jira_url = "https://your_jira_instance.atlassian.net/rest/api/2/search"
jira_auth = ('your_username', 'your_api_token')

# JQL query to check if a ticket exists in the last 24 hours
jql_query = 'labels="LOGS_MISSING" AND labels="feed_name1" AND created >= -24h'
response = requests.get(jira_url, params={'jql': jql_query}, auth=jira_auth)

# If a ticket exists
if response.json()['issues']:
    ticket_key = response.json()['issues'][0]['key']
    print(f"Ticket {ticket_key} already exists.")
    # Optionally update ticket here
else:
    # No ticket found, create a new one
    create_url = "https://your_jira_instance.atlassian.net/rest/api/2/issue"
    new_ticket_data = {
        "fields": {
           "project": {
              "key": "YOUR_PROJECT_KEY"
           },
           "summary": "Alert: LOGS_MISSING for feed_name1",
           "description": "The feed 'feed_name1' did not receive expected logs. Severity: 4, Priority: 6.",
           "issuetype": {
              "name": "Task"
           },
           "labels": ["LOGS_MISSING", "feed_name1"],
           "customfield_10000": "SOC_VFUK_UC_L3_00001"  # Alert ID
        }
    }
    create_response = requests.post(create_url, json=new_ticket_data, auth=jira_auth)
    print(f"Created new ticket: {create_response.json()['key']}")
