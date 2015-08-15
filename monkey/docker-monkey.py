from plumbum import local
from time import sleep
from random import sample
from monkeylib import resolve_func

import numpy
import yaml
import inspect


docker = local["docker"]

dead_time = dict()
alive_time = dict()


conf_file = file('conf.yaml', 'r')
config = yaml.load(conf_file)


func_trail = resolve_func(config['trail'])
func_rescue = resolve_func(config['rescue'])


cycle = 0
#Main loop
while True :
  print '\n========%d========' % cycle
  cycle += 1

  alives = docker[ "ps", "-q" ]().split()
  all_containers = docker[ "ps", "-a" , "-q"]().split()

  deads = []


  for c in all_containers:
    if not c in alives:
      deads.append(c)

  print 'Running: %s' % alives
  print 'Stopped: %s' % deads


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
  print 'To stop: %s' % tostop
  print 'To start: %s' % tostart

  for c in tostop:
    docker["stop"].popen(c)

  for c in tostart:
    docker["start"].popen(c)
  

  sleep(config['interval'])

