from plumbum import local
from time import sleep
from random import sample
from monkeylib import resolve_func, add_to_container_meta, container_names

import numpy
import yaml
import inspect
import sys
from monkeylog import Logger

docker = local["docker"]

dead_time = dict()
alive_time = dict()

try:
  config_file_path = sys.argv[1]
except:
  config_file_path = 'conf.yaml'

conf_file = file(config_file_path, 'r')
config = yaml.load(conf_file)


func_trail = resolve_func(config['trail'])
func_rescue = resolve_func(config['rescue'])

logger = Logger(config_file_path.split('/')[-1].split(".")[0])

cycle = 0
#Main loop
while True :
  print '\n========%d========' % cycle
  logger.new_cycle(cycle)
  cycle += 1

  alives = docker[ "ps", "-q" ]().split()
  all_containers = docker[ "ps", "-a" , "-q"]().split()

  deads = []


  for c in all_containers:
   add_to_container_meta(c) 
   if not c in alives:
      deads.append(c)

  print 'Running: %s' % container_names(alives)
  print 'Stopped: %s' % container_names(deads)
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
  logger.log("tostop", container_names(tostop))
  logger.log("tostart", container_names(tostart))

  for c in tostop:
    docker["stop"].popen(c)

  for c in tostart:
    docker["start"].popen(c)
  
  logger.flush()
  sleep(config['interval'])

