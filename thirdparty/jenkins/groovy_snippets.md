### Groovy Snippets

- Cut a portion
```
"${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/')[2].split('\\.')}"
```


- Branch checks with regex pattern
```
MY_BRANCH="feature/correct-pattern"
def branches = [ "main", "feature/.*"]
if (branches.any{ branch -> MY_BRANCH ==~ branch}) {
    println("MY_BRANCH adheres to pattern")
} 
else {
    println("MY_BRANCH NOT adhere to pattern")
    currentBuild.result = 'ABORTED'
    error('Quitting due to NON-pattern match')
}

```


- Skip a stage based on boolean value
```
when { excpression {return params.SKIP_STAGE_3 }}
```