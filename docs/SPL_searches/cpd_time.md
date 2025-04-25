### cpd time Examples

```
# Replicated Current Processing Day (CPD) at search time
<mySearch>
| rename _time as myTime
| table myTime, hosts, sourcetype
| convert timeformat="%H" ctime(myTime) as hr
| convert timeformat="%M" ctime(myTime) as min
| convert timeformat="%S" ctime(myTime) as sec
| convert timeformat="%w" ctime(myTime) as wday
| eval day=(myTime - (hr*60*60) - (min * 60) - sec)
| eval secs=((hr*60*60)+(min*60)+sec)
| eval adjustedTime = if((secs < (8*60*60)), (day + (8*60*60)), myTime)
| eval adjustedTime = if((secs > (17*60*60)), (day + 86400 + (8*60*60)), adjustedTime)
| eval adjustedTime = if(((secs > (17*60*60)) AND (wday=5)), (day + (3*86400) + (8*60*60)), adjustedTime)
| eval adjustedTime = if((wday=0), (day + (1*86400) + (8*60*60)), adjustedTime)
| eval adjustedTime = if((wday=6), (day + (2*86400) + (8*60*60)), adjustedTime)
| convert timeformat="%H:%M %a %d/%m/%Y" ctime(myTime) as myTimeT
| convert timeformat="%H:%M %a %d/%m/%Y" ctime(day) as dayT
| convert timeformat="%H:%M %a %d/%m/%Y" ctime(adjustedTime) as adjustedTimeT
```
