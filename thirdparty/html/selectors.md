## Various Selectors

```
#xpath
/html/body/table/tbody/tr[1]/td[2]/span

# Selector 
body > table > tbody > tr:nth-child(1) > td:nth-child(2) > span

# JS path
document.querySelector("body > table > tbody > tr:nth-child(1) > td:nth-child(2) > span")
```

### CSS Selector Conditionals
```
# If contains style*=ff0000 within span
body > table > tbody > tr:nth-child(2) > td>span[style*=ff0000]

```
