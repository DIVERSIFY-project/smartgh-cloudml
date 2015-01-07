FROM consol/tomcat-7.0
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update && apt-get install -y maven git wget
RUN cd /opt && git clone https://github.com/DIVERSIFY-project/SMART-GH.git ./gh
RUN cd /opt/gh/maps && bash get-dublinmap.sh
RUN cd /opt/gh && echo -e '\n cd /opt/gh \n bash set-redis-url.sh --url $redisurl \n cd /opt/gh/ \n mvn clean \n mvn -DskipTests install \n cd daemon-wservice/ \n mvn package \n mkdir /maven \n cd target/ \n cp restful-graphhopper-1.0.war /maven/ \n /opt/tomcat/bin/deploy-and-run.sh' > run_hopper.sh
