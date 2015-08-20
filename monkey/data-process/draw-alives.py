import matplotlib.pyplot as plt
import yaml
import sys

def line(x1,y1,x2,y2):
  plt.plot([x1,x2],[y1,y2], '-')

try:
  logfile = sys.argv[1]
except:
  logfile = "log.yaml"

found = 0
ids = dict()

def toid(name):
  global found
  global ids
  if name in ids:
    return ids[name]
  ids[name] = found
  found += 1

f = open(logfile, "r")
for item in yaml.load_all(f):
  cycle = item['cycle']
  for c in item['running']:
    id = toid(c)
    line(cycle, id, cycle+1, id)
plt.show()

