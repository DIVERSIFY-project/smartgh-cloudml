#! /usr/bin/python

from plumbum import local
from time import sleep
from random import sample
from monkeylib import *
import monkeyws
import os
import numpy
import yaml
import inspect
import sys
import time
import datetime
from monkeylog import Logger

docker = local["docker"]

dead_time = dict()
alive_time = dict()

try:
  config_file_path = sys.argv[-1]
  if config_file_path.endswith('py'):
    raise Exception('need a yaml file')
except:
  config_file_path = './conf.yaml'

conf_file = file(config_file_path, 'r')
config = yaml.load(conf_file)
interval = config['interval']

if '-i' in sys.argv:
  interval = sys.argv[sys.argv.index('-i')+1]

if '-m' in sys.argv:
  meta_file_path = sys.argv[sys.argv.index('-m')+1]
else:
  meta_file_path = './meta.yaml'

init_static_meta(meta_file_path)

func_trail = resolve_func(config['failure'])
func_rescue = resolve_func(config['recovery'])

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('-%Y%m%d-%H%M%S')
logger = Logger(config_file_path.split('/')[-1].split(".")[0]+timestamp)

all_containers = docker["ps", "-a", "-q"]().split()
metas = get_static_metas()

for c in all_containers:
 add_to_container_meta(c)

all_containers_name = container_names(all_containers)
print all_containers_name

for c in metas:
  if not(c in all_containers_name):
    print docker("run", "-d", "-p", "%d:8080" % metas[c]["port"], "--name", c, "songhui/smhp-hopper-jetty")

cycle = 0
#Main loop
while True :

  if interval == "tick_websocket":
    while True:
      sleep(0.1)
      if monkeyws.tick:
        monkeyws.tick = False
        break
  elif interval == "tick_keyboard":
    raw_input("press <Enter> to continue...")
  elif type(interval) is int:
    interval_i = int(interval)
    sleep(interval_i)
    

  print '\n========%d========' % cycle
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
  alives = [x for x in alives if container_name(x) in get_static_metas()]
  deads = [x for x in deads if container_name(x) in get_static_metas()]

  print 'Running: %s' % container_names(alives)
  print 'Stopped: %s' % container_names(deads)
  logger.log('running', container_names(alives))
  logger.log('stopped', container_names(deads))
  
  alive_services = set()
  for c in alives:
    for s in get_static_metas()[container_name(c)]['services']:
      alive_services.add(s)

  logger.log("alive_services", list(alive_services))

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
  logger.log("tostop", container_names(tostop))
  logger.log("tostart", container_names(tostart))

  for c in tostop:
    docker["pause"].popen(c)

  for c in tostart:
    docker["unpause"].popen(c)
  
  logger.flush()

