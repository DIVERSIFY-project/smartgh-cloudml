#! /usr/bin/python

from plumbum import local
from time import sleep
from random import sample
from monkeylib import *
#import monkeyws
import monkeyws_client
import os
import numpy
import yaml
import inspect
import sys
import time
import datetime
from monkeylog import Logger
from kazoo.client import KazooClient
import random 
useLogger = False

docker = local["docker"]

dead_time = dict()
alive_time = dict()

try:
  config_file_path = sys.argv[-1]
  if not config_file_path.endswith('yaml'):
    raise Exception('config file needs to be a .yaml file')
except:
  config_file_path = './conf.yaml'

conf_file = file(config_file_path, 'r')
config = yaml.load(conf_file)
interval = config['interval']

if '-i' in sys.argv:
  interval = sys.argv[sys.argv.index('-i')+1]

if '-a' in sys.argv:
  ipaddress = sys.argv[sys.argv.index('-a')+1]
else:
  ipaddress = 'localhost'
  print 'No IP address specified (use -a), using localhost'

if '-z' in sys.argv:
  monkey_id = '%032x' % random.getrandbits(128) 
  zookeeper_addr = sys.argv[sys.argv.index('-z')+1]
  zookeeper = KazooClient(hosts=zookeeper_addr)
  zookeeper.start()
  zookeeper.ensure_path('monkey/%s/tick' % monkey_id)  

#monkeyws_client.connect(ipaddress)

func_trail = resolve_func(config['failure'])
func_rescue = resolve_func(config['recovery'])

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('-%Y%m%d-%H%M%S')
if useLogger:
  logger = Logger(config_file_path.split('/')[-1].split(".")[0]+timestamp)

all_containers = docker["ps", "-a", "-q"]().split()

for c in all_containers:
 add_to_container_meta(c)

all_containers_name = container_names(all_containers)
print all_containers_name


cycle = 0
#Main loop
while True :

  if interval == "tick_websocket":
    while True:
      sleep(0.1)
      if monkeyws_client.tick:
        monkeyws_client.tick = False
        break
  elif interval == "tick_zookeeper":
    if not zookeeper:
      print "Zookeeper address is not set-up. Use  -z host:port"
      exit()
    while True:
      sleep(0.1)
      if zookeeper.get('/monkey/%s/tick'%monkey_id)[0]==b't':
        zookeeper.set('/monkey/%s/tick'%monkey_id, b't')
        print 'got a tick from zookeeper'
        break
  elif interval == "tick_keyboard":
    raw_input("press <Enter> to continue...")
  elif type(interval) is int:
    interval_i = int(interval)
    sleep(interval_i)
    

  print '\n========%d========' % cycle
  if useLogger:
    logger.new_cycle(cycle)
  cycle += 1

  alives = docker[ "ps", "-q", "-f", "status=running" ]().split()
  all_containers = docker[ "ps", "-a" , "-q"]().split()

  deads = []


  for c in all_containers:
   add_to_container_meta(c) 
   if not c in alives:
      deads.append(c)

  #print get_static_metas()

  print 'Running: %s' % container_names(alives)
  print 'Stopped: %s' % container_names(deads)
  if useLogger:
    logger.log('running', container_names(alives))
    logger.log('stopped', container_names(deads))
  

  for c in alives:
    dead_time.pop(c, None)
    if not c in alive_time:
      alive_time[c] = 0
    else:
      alive_time[c] += 1


  for c in deads:
    alive_time.pop(c, None)
    if not c in dead_time:
      dead_time[c] = 0
    else:
      dead_time[c] += 1



  #print alive_time
  #print dead_time
   
  tostop = func_trail(alive_time)
  tostart = func_rescue(dead_time)
  print 'To stop: %s' % container_names(tostop)
  print 'To start: %s' % container_names(tostart)
  if useLogger:
    logger.log("tostop", container_names(tostop))
    logger.log("tostart", container_names(tostart))

  for c in tostop:
    docker["pause"].popen(c)

  for c in tostart:
    docker["start"].popen(c)
    docker["unpause"].popen(c)

  if useLogger:
    logger.flush()

