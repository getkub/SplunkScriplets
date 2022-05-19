# regex in if loop
if [[ "$action" =~ ^(apple|mango|pine|straw)$ ]]
then
    echo "Fruit=${action}"
else
    echo "ERROR: Not in desired list "
    exit 100
fi
