import requests
from datetime import datetime, timedelta

# Jira URL and Authentication setup
jira_url = "https://your_jira_instance.atlassian.net/rest/api/2/search"  # JIRA search endpoint
jira_auth = ('your_username', 'your_api_token')  # Replace with your Jira username and API token

# Function to check if a ticket with the same rule_id and feed_name already exists
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
    # JQL query to find tickets with the same rule_id, feed_name, and created in the last 24 hours
    jql_query = f'labels="{rule_id}" AND labels="{feed_name}" AND created >= -24h'
    
    # Send GET request to JIRA API to search for matching tickets
    response = requests.get(jira_url, params={'jql': jql_query}, auth=jira_auth)
    
    if response.status_code == 200:
        issues = response.json().get('issues', [])
        if issues:
            # If matching tickets are found, return the ticket key of the first one
            return issues[0]['key']
    else:
        # Handle error if the request to JIRA fails
        print(f"Error querying JIRA: {response.status_code} - {response.text}")
    
    # Return None if no matching ticket is found
    return None

# Function to create a new ticket in Jira
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
    create_url = "https://your_jira_instance.atlassian.net/rest/api/2/issue"  # JIRA issue creation endpoint
    
    # Data payload for creating the new ticket
    new_ticket_data = {
        "fields": {
            "project": {
                "key": "YOUR_PROJECT_KEY"  # Replace with your project key (e.g., "SOC")
            },
            "summary": f"Alert: {rule_id} for {feed_name}",
            "description": description,
            "issuetype": {
                "name": "Task"  # Assuming Task is the issue type, modify if needed
            },
            "labels": [rule_id, feed_name]  # Labels for easy search
        }
    }

    # Send POST request to create the new Jira ticket
    create_response = requests.post(create_url, json=new_ticket_data, auth=jira_auth)
    
    if create_response.status_code == 201:
        # Return the ticket key if the creation was successful
        return create_response.json()['key']
    else:
        # Print error if ticket creation fails
        print(f"Failed to create ticket: {create_response.status_code} - {create_response.text}")
    
    # Return None if ticket creation failed
    return None

# Function to append a comment to an existing ticket
def append_to_ticket(ticket_key, message):
    """
    Appends a comment to an existing JIRA ticket.

    Args:
        ticket_key (str): The JIRA ticket key to which the comment should be added.
        message (str): The message to be added as a comment.
    """
    comment_url = f"https://your_jira_instance.atlassian.net/rest/api/2/issue/{ticket_key}/comment"  # Comment endpoint
    
    # Data payload for adding a comment
    comment_data = {
        "body": message  # The message content to be added as the comment
    }
    
    # Send POST request to append the comment to the ticket
    comment_response = requests.post(comment_url, json=comment_data, auth=jira_auth)
    
    if comment_response.status_code != 201:
        # Print error if comment appending fails
        print(f"Failed to add comment to ticket {ticket_key}: {comment_response.status_code} - {comment_response.text}")

# Main function to handle ticket creation and comment appending
def handle_ticket(rule_id, feed_name, description, child_alert_message):
    """
    Handles ticket creation or comment appending based on whether a matching ticket exists.
    If a ticket is found, it appends the child alert message as a comment. If not, it creates
    a new ticket.

    Args:
        rule_id (str): The rule identifier associated with the alert.
        feed_name (str): The feed index name (e.g., feed_name1).
        description (str): The description of the alert.
        child_alert_message (str): The message to be appended as a comment.
    """
    # Check for an existing ticket based on rule_id and feed_name within 24 hours
    ticket_key = get_existing_ticket(rule_id, feed_name)
    
    if ticket_key:
        # If a matching ticket exists, append the child alert as a comment
        print(f"Ticket {ticket_key} already exists.")
        append_to_ticket(ticket_key, child_alert_message)
    else:
        # If no matching ticket exists, create a new ticket
        print("No existing ticket found, creating a new one.")
        new_ticket_key = create_new_ticket(rule_id, feed_name, description)
        
        if new_ticket_key:
            # If ticket creation is successful, print the new ticket key
            print(f"Created new ticket: {new_ticket_key}")
            # Optionally append the child alert as a comment to the new ticket
            append_to_ticket(new_ticket_key, child_alert_message)

# Example usage
rule_id = "RULE01"  # The rule ID (e.g., LOGS_MISSING)
feed_name = "feed_name1"  # The feed index (e.g., feed_name1)
description = "The feed 'feed_name1' did not receive expected logs. Severity: 4, Priority: 6. Please investigate."
child_alert_message = "Child alert: Missing logs for device X in feed_name1."

# Call the function to handle the ticket
handle_ticket(rule_id, feed_name, description, child_alert_message)
