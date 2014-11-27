The cloudml model and some scripts for deployment smart-graghhopper.

Manually deploy SmartGH with docker:
==========

```bash
#deploy redis, currently redis has to be mapped only to 6379
sudo docker run -d -p 6379:6379 redis

#deploy sensor processor <redis_ip> is in the form like 192.168.1.11, i.e., pure ip without port
sudo docker run -d -e "redisurl=<redis_ip>" songhui/smhp-sensor /bin/bash /opt/gh/run_sensor.sh

#deploy web services
sudo docker run -d -e "redisurl=<redis_ip>" -p 8080:8080 songhui/smhp-hopper-tomcat /bin/bash /opt/gh/run_hopper.sh

#deploy website, <ws_url> is in the form like http://192.168.1.11:8080
sudo docker run -d -e "WS_CONFIG=<ws_url>" -p 80:8989 songhui/smhp-web /bin/bash /opt/gh/run_web.sh
```

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
