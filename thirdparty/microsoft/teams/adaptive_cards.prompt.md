You are an expert in Microsoft Teams Adaptive Cards and workflow automation.

Create a complete, production-ready Adaptive Card JSON for an approval workflow with the following requirements:

* Title: "Approval Request"

* Display dynamic request details including:

  * Request title
  * Requester name
  * Department
  * Amount
  * Date

* Use a clean layout with appropriate spacing and emphasis (e.g., bold title, FactSet for metadata)

* Include an optional multiline comment input field

  * Input id should be "comment"

* Include two action buttons:

  1. Approve (style: positive)
  2. Reject (style: destructive)

* Each button must:

  * Use Action.Submit
  * Include a data payload with:

    * "action": "approve" or "reject"
    * "request_id": dynamic variable

* Use templating placeholders compatible with Tines (e.g., {{request.title}}, {{request.id}})

* Ensure the JSON is valid for Microsoft Teams (Adaptive Card schema version 1.4 or later)

* Follow best practices:

  * Proper spacing between elements
  * Readable and structured layout
  * No unnecessary fields
  * Compatible with Power Automate or webhook delivery

Return only the final JSON payload with no explanation.
