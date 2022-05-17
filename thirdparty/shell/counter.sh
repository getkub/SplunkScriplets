baseURL="https://someDir/"
count=32
i=1

while [ $i -le $count ]
do
if [ $i -lt 10 ]; then
pad=0
else
pad=""
fi

echo curl -o ${pad}${i}.mp3 "${baseURL}/${pad}${i}.mp3" 
i=$((i+1))
done 
