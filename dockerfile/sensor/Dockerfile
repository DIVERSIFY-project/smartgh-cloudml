FROM songhui/smhp-base
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update && apt-get install -y python-pip
RUN cd /opt/gh && pip install -r requirements.txt
RUN cd /opt/gh && echo 'cd /opt/gh; bash set-redis-url.sh --url $redisurl; cd sensor_processing; python process_sensor_data_daemon.py' > run_sensor.sh
