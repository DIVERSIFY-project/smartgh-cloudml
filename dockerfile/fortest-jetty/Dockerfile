FROM jetty:jre7
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update \
	&& apt-get install -y openjdk-7-jdk maven git python-plumbum zip\
	&& cd /opt \
	&& git clone https://github.com/DIVERSIFY-project/SMART-GH.git \
	&& cd /opt/SMART-GH/ \
	&& git checkout demo \
	&& python generate_config.py --city dublin --sensors GoogleTraffic,NoiseTube,OzoneDetect --modes car,bike \
	&& cd maps \
	&& wget http://thingml.org/dist/diversify/dublin-m50.osm && mv dublin-m50.osm dublin.osm \
	&& wget http://thingml.org/dist/diversify/dublin-gh.zip \
	&& unzip dublin-gh.zip -d dublin-gh \
	&& cd /opt/SMART-GH/ \
	&& mvn clean \
	&& mvn -DskipTests install \
	&& cd daemon-wservice \
	&& mvn package \
	&& cp target/restful-graphhopper-1.0.war $JETTY_HOME/webapps \
	&& apt-get --purge autoremove -y maven git\
	&& rm -rf /opt/SMART-GH/ \
	&& cd / \
        && echo "cd $JETTY_HOME; java -jar start.jar" > run.sh \
	&& chmod a+x /run.sh

CMD /run.sh
