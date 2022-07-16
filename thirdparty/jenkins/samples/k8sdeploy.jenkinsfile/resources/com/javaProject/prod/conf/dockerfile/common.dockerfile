FROM ${harbor_host}/ehome/java:${JDK_V}
MAINTAINER deployer
WORKDIR ${target_dir}/target/
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
COPY *.jar /opt/${Service}.jar
ADD http://172.24.114.94:8080/MySources/Linux/Monitor/ELK/plugins/elastic-apm-agent-1.12.0.jar /opt/
EXPOSE ${Port}
ENTRYPOINT $dockerFile_start