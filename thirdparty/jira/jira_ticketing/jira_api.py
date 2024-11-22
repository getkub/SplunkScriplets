# jira_api.py
import requests
from config import JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN

# Function to query JIRA and check if a ticket already exists based on rule_id and feed_name
def get_existing_ticket(rule_id, feed_name):
    """
    Queries JIRA to check if a ticket already exists for the given rule_id and feed_name 
    created within the last 24 hours.

    Args:
        rule_id (str): The rule identifier associated with the alert (e.g., LOGS_MISSING).
        feed_name (str): The name of the feed index (e.g., feed_name1).

    Returns:
        str: The JIRA ticket key if a matching ticket is found, else None.
    """
    jql_query = f'labels="{rule_id}" AND labels="{feed_name}" AND created >= -24h'
    response = requests.get(f"{JIRA_URL}/rest/api/2/search", params={'jql': jql_query}, auth=(JIRA_USERNAME, JIRA_API_TOKEN))

    if response.status_code == 200:
        issues = response.json().get('issues', [])
        if issues:
            return issues[0]['key']
    else:
        print(f"Error querying JIRA: {response.status_code} - {response.text}")
    return None

# Function to create a new ticket in JIRA
def create_new_ticket(rule_id, feed_name, description):
    """
    Creates a new ticket in JIRA if no existing ticket is found.

    Args:
        rule_id (str): The rule identifier associated with the alert.
        feed_name (str): The feed index name (e.g., feed_name1).
        description (str): The description of the alert to be included in the ticket.

    Returns:
        str: The JIRA ticket key of the newly created ticket if successful, else None.
    """
    new_ticket_data = {
        "fields": {
            "project": {
                "key": "YOUR_PROJECT_KEY"  # Replace with your actual project key
            },
            "summary": f"Alert: {rule_id} for {feed_name}",
            "description": description,
            "issuetype": {
                "name": "Task"  # Modify issue type if needed
            },
            "labels": [rule_id, feed_name]
        }
    }

    create_response = requests.post(f"{JIRA_URL}/rest/api/2/issue", json=new_ticket_data, auth=(JIRA_USERNAME, JIRA_API_TOKEN))

    if create_response.status_code == 201:
        return create_response.json()['key']
    else:
        print(f"Failed to create ticket: {create_response.status_code} - {create_response.text}")
    return None

# Function to append a comment to an existing JIRA ticket
def append_to_ticket(ticket_key, message):
    """
    Appends a comment to an existing JIRA ticket.

    Args:
        ticket_key (str): The JIRA ticket key to which the comment should be added.
        message (str): The message to be added as a comment.
    """
    comment_data = {
        "body": message
    }

    comment_response = requests.post(f"{JIRA_URL}/rest/api/2/issue/{ticket_key}/comment", json=comment_data, auth=(JIRA_USERNAME, JIRA_API_TOKEN))

    if comment_response.status_code != 201:
        print(f"Failed to add comment to ticket {ticket_key}: {comment_response.status_code} - {comment_response.text}")
