## Find all alert actions

```
| rest /services/alerts/alert_actions
| table title, command, eai:acl.app, description

```

