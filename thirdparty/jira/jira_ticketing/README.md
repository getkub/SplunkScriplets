### Explanation of Each File
- config.py - Contains configuration values like JIRA URL, authentication credentials, etc.
- jira_api.py - Contains functions for interacting with the JIRA API (querying for tickets, creating tickets, and adding comments).
- ticket_handler.py - Contains the logic for handling ticket creation, querying, and appending comments (main logic).
- main.py - Entry point to run the program and invoke the functions.


### Requirements
```
pip install requests
```

### How to run
```
python main.py
```