### for each Examples

```
# For_each tricky searches

# https://answers.splunk.com/answers/519459/only-show-null-values-from-timechart-valuessource.html 
... | foreach * [eval shouldAlert=shouldAlert+if(isnull('<<FIELD>>') OR '<<FIELD>>'="",1,0)] | whereshouldAlert>0
```
