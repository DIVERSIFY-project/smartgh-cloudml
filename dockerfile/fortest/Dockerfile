FROM consol/tomcat-7.0
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update; apt-get install -y maven; cd /opt; git clone https://github.com/DIVERSIFY-project/SMART-GH.git; cd SMART-GH/; wget http://thingml.org/dist/diversify/dublin-m50.osm; cd /opt/SMART-GH; mvn clean; mvn -DskipTests install; cd daemon-wservice; mvn package; cp target/restful-graphhopper-1.0.war /opt/tomcat/webapps/; cd /; /opt/tomcat/bin/startup.sh; curl http://127.0.0.1:8080/restful-graphhopper-1.0/hello; /opt/tomcat/bin/shutdown.sh; rm /opt/tomcat/webapps/restful-graphhopper-1.0.war; apt-get --purge autoremove maven; rm -rf /opt/SMART-GH/; echo "/opt/tomcat/bin/startup.sh; tail -f /opt/tomcat/logs/catalina.oht">/run.sh; chmod a+x /run.sh

CMD /run.sh

