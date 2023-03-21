### Groovy Snippets

- Cut a portion
```
"${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/')[2].split('\\.')}"
```