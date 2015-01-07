FROM songhui/smhp-base
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update && apt-get install -y openjdk-7-jdk maven
RUN cd opt/gh && mvn -DskipTests package
RUN cd /opt/gh ; echo -e '\n cd /opt/gh; ./smartghweb.sh web \n while [ 1 ] \n do \n sleep 1000 \n done' > run_web.sh
