addr = ["10.5","10.5","10.7"]
addr.each{println it}

numlist = [10,11,12]
numlist.each{println it}



//this is list
addrlist = ["10.0.0.1","10.0.0.2","10.0.0.3"]
//this is string type
env.addrString = ["10.0.0.1","10.0.0.2","10.0.0.3"]

String smallScope = "smallScope: only this file can use" //带String时,jenkinsfile引用会抛异常，本文件内可用
def smallScope02 = "smallScope2: only this file can use" //带def时,jenkinsfile引用会抛异常，本文件内可用

abc = "abc: this is global String"

abcPms = " ${abc} , abcPms: and test abc parmas"
abcPms02 = abc + ", abcPms02: and test abc parmas"

testString = "${smallScope},testString: can use in here"
testString02 = smallScope + ",testString: can use in here"


println(smallScope)
println(abc)
println(abcPms)
println(abcPms02)
println(testString)
println(testString02)
println(smallScope02)
println("addrString: " + addrString.getClass())
println("addrlist: " + addrlist.getClass())

harbor_host = "10.0.0.1"
JDK_V = "8"
Service = "test"
Port = "32161"
java_Xms = "1g"
java_Xmx = "1g"
java_Xmn = "512m"
MemConf = "-Xms${java_Xms} -Xmx${java_Xmx} -Xmn${java_Xmn}"
JAVA_OPTS = "-server ${MemConf} -XX:SurvivorRatio=8 -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m -XX:+UseParallelGC -XX:ParallelGCThreads=4 -XX:+UseParallelOldGC -XX:+UseAdaptiveSizePolicy -XX:+PrintGCDetails -XX:+PrintTenuringDistribution -XX:+PrintGCTimeStamps -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/ -Xloggc:/gc.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=5 -XX:GCLogFileSize=10M"
dockerFile_start = "java ${JAVA_OPTS} -Dserver.port=${Port} -Djava.security.egd=file:/dev/./urandom -jar /opt/${Service}.jar"

