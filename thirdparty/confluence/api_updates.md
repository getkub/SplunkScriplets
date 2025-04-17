## API updates

- uses Huachao Mao REST Client plugin in Visual studio (Ctrl+Alt_R in Windows or Cmd+Alt+R in MacOS)

```
PUT {{baseUrl}}/wiki/api/v2/pages/3327557500
Content-Type: application/json
Accept: application/json
Authorization: Basic {{token_b64}}

<@ ./content.json
```

- content.json is below


```
{
  "id": "3327557500",
  "title": "sample Update",
  "body": {
    "representation": "storage",
    "value": "<h2>Notes</h2><body>sample</body>"
  },
  "version": {
    "number": 2,
    "message": "Updated with Markdown"
  }
}
```
