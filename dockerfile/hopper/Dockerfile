FROM songhui/smhp-base
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update && apt-get install -y openjdk-7-jdk maven
RUN cd opt/gh && mvn -DskipTests package
RUN cd /opt/gh && echo 'cd /opt/gh; bash set-redis-url.sh --url $redisurl; ./graphhopper.sh web ./maps/dublin-m50.osm' > run_hopper.sh
