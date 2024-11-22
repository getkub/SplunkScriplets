# main.py
from ticket_handler import handle_ticket

# Example usage
rule_id = "RULE01"  # The rule ID (e.g., LOGS_MISSING)
feed_name = "feed_name1"  # The feed index (e.g., feed_name1)
description = "The feed 'feed_name1' did not receive expected logs. Severity: 4, Priority: 6. Please investigate."
child_alert_message = "Child alert: Missing logs for device X in feed_name1."

# Call the function to handle the ticket
handle_ticket(rule_id, feed_name, description, child_alert_message)
