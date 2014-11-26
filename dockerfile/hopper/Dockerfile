FROM songhui/smhp-web
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update && apt-get install -y tomcat7 openjdk-7-jdk maven
RUN cd opt/gh ; mvn -DskipTests install ; cd daemon-wservice/ ; mvn package ; cp target/restful-graphhopper-1.0.war /var/lib/tomcat7/webapps/
RUN cd /opt/gh && echo -e '/etc/init.d/tomcat7 start; cd /opt/gh; bash set-redis-url.sh --url $redisurl; \n while [ 1 ] \n do \n sleep 1000 \n done' > run_hopper.sh
