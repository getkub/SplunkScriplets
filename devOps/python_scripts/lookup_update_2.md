# Idea on how to update CSV/lookup automatically without lookup editor

```
STACK="https://yourstackname.splunkcloud.com"
MY_LOOKUP="test_csv.csv"
TOKEN='12345'
GITHUB_RAW_URL="https://raw.githubusercontent.com/test/csvtest/main/${MY_LOOKUP}"


## pull csv
csv_raw=$(curl -sL "${GITHUB_RAW_URL}")
csv_escaped=$(printf '%s\n' "$csv_raw" | sed 's/"/\\"/g')

## Write SPL logic

read -r -d " SPL <<EOF
| makeresults format=csv data="
$csv_escaped"
|outputlookup ${MY_LOOKUP}
EOF


## Run the search to search/jobs endpoint

curl -s -k -X POST \
-H "Authorization: Bearer ${TOKEN} \
--data-urlencode search="$SPL" \
"${STACK}:8089/services/search/jobs"

```