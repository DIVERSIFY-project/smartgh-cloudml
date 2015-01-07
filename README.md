The cloudml model and some scripts for deployment smart-graghhopper.

Manually deploy SmartGH with docker:
==========

```bash
#deploy redis, currently redis has to be mapped only to 6379
sudo docker run -d -p 6379:6379 redis

#deploy sensor processor, replace 192.168.11.20 with the ip where you deploy redis, no port
sudo docker run -d -e "redisurl=192.168.11.20" songhui/smhp-sensor /bin/bash /opt/gh/run_sensor.sh

#deploy web service, the first 8080 is changeable
sudo docker run -d -e "redisurl=192.168.11.20" -p 8080:8080 songhui/smhp-hopper-tomcat /bin/bash /opt/gh/run_hopper.sh

#deploy website, replace http://192.168.11.22:8080 with the url where you deploy the web service, with a port this time, and do not forget "http://", the port 80 is changeable
sudo docker run -d -e "WS_CONFIG=http://192.168.11.21:8080" -p 80:8989 songhui/smhp-web /bin/bash /opt/gh/run_web.sh
```

Now you should be able to use the web-based ui via http://192.168.11.22:80, suppose 192.168.11.22 is where you deploy the website

Build docker images yourself
===================

``` bash
git clone https://github.com/DIVERSIFY-project/smartgh-cloudml.git
cd smartgh-cloudml/dockerfile/
bash build.sh
```

Deploy automatically using CloudML
==================================

This currently only works on SINTEF's minicloud. For other platforms, you need to edit the cloudml model, using [cloudml-dsl](https://github.com/SINTEF-9012/cloudml-dsl), or directly on the model/diversify/src-gen/SmartGH.json

``` bash
git clone https://github.com/SINTEF-9012/cloudml.git
cd cloudml
mvn clean install
cd ui/shell/target
java -jar cloudml-shell.jar
```
inside cloudml:
```
load deployment from <git repos of smartgh-cloudml>/model/diversify/src-gen/SmartGH.json
deploy
```
