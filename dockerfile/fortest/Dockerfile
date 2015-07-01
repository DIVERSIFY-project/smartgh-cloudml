FROM consol/tomcat-7.0
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update; apt-get install -y maven; cd /opt; git clone https://github.com/DIVERSIFY-project/SMART-GH.git; cd /opt/SMART-GH/; git checkout demo; cd maps; wget http://thingml.org/dist/diversify/dublin-m50.osm; cd /opt/SMART-GH/; mvn clean; mvn -DskipTests install; cd daemon-wservice; mvn package; cp target/restful-graphhopper-1.0.war /opt/tomcat/webapps/; cd /; /opt/tomcat/bin/startup.sh; while true; do if curl -v --silent http://127.0.0.1:8080/restful-graphhopper-1.0/hello --stderr - | grep "Tallaght"; then break; fi; sleep 10; echo "Wait for tomcat to really start"; done; echo "finished"; /opt/tomcat/bin/shutdown.sh; rm /opt/tomcat/webapps/restful-graphhopper-1.0.war; apt-get --purge autoremove -y maven; rm -rf /opt/SMART-GH/; echo "/opt/tomcat/bin/startup.sh; tail -f /opt/tomcat/logs/catalina.out">/run.sh; chmod a+x /run.sh

CMD /run.sh

