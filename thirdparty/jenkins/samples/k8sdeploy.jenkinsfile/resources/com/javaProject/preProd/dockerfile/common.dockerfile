FROM ${harbor_host}/ehome/java:${JDK_V}
MAINTAINER deployer
WORKDIR ${target_dir}/target/
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
COPY *.jar /opt/${Service}.jar
EXPOSE ${Port}
ENTRYPOINT ${dockerFile_start}