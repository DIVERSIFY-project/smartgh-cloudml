from plumbum import local
from time import sleep
from random import sample

import numpy
import yaml
import inspect

def resolve_func(func_config):
  if type(func_config) is str:
    return lambda : func_config

docker = local["docker"]

dead_time = dict()
alive_time = dict()


conf_file = file('conf.yaml', 'r')
config = yaml.load(conf_file)



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
  result = dict()
  for trail_or_rescue in ['trail', 'rescue']:
    conf = config[trail_or_rescue]  
    exec('import %s' % conf['file'])
    func = eval('%s.%s'%(conf['file'], conf['function']))


    arg_names = inspect.getargspec(func)[0]
    args = dict()  
    for x in arg_names:
      if x in conf:
        args[x] = conf[x]
    if trail_or_rescue == 'trail':
      args['containers_time'] = alive_time
    else:
      args['containers_time'] = dead_time
    
    result[trail_or_rescue] = func(**args)
   
  tostop = result['trail']
  tostart = result['rescue']
  print 'To stop: %s' % tostop
  print 'To start: %s' % tostart

  for c in tostop:
    docker["stop"].popen(c)

  for c in tostart:
    docker["start"].popen(c)
  

  sleep(config['interval'])

