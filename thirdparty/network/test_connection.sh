# Test various levels of connectivity
# Can your laptop connect to VPN, then to intranet site, then to final URL etc.

outputFile="/tmp/connectionTest.log"
a=1
url1="https://google.com"
url2="https://not-reachable-somesite_outthere.com"
url3="https://facebook.com"
sleepSeconds="60"

while [ $a -lt 200 ]; do

  runID=`date +%s`
  urls=( "$url1", "$url2", "$url3" )

   for url in "${urls[@]}"
   do
	    curl -s --connect-timeout 2 -o /dev/null $url
      echo "runID=$runID url=$url rc=$? runTime="`date +%FT%T` >> ${outputFile}
   done
  a=`expr $a + 1`
  sleep $sleepSeconds
done
