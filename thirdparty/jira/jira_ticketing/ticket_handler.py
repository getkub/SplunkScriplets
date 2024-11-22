# ticket_handler.py
from jira_api import get_existing_ticket, create_new_ticket, append_to_ticket

# Function to handle ticket creation and comment appending
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
