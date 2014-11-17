#Will be used to create the basic image from the latest smart-gh repository

FROM ubuntu:14.04 
MAINTAINER Hui Song <hui.song@sintef.no>

RUN apt-get update && apt-get install -y git wget
RUN cd /opt && git clone https://github.com/DIVERSIFY-project/SMART-GH.git ./gh
RUN cd /opt/gh/maps && bash get-dublinmap.sh
RUN apt-get remove -y git wget


