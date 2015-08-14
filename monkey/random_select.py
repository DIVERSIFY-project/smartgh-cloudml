import numpy
import random


def random_select(containers_time, dist_name, dist_paras):
  if len(containers_time) == 0:
    return []
  number = 0
  try:
    number = paras["number"]
  except Exception as e:
    number = 1

  dist_fun = eval("numpy.random."+dist_name)

  if 'size' in dist_paras:
    del dist_paras['size']
  num_to_select = dist_fun(**dist_paras)
  if num_to_select >= len(containers_time.keys()):
    return containers_time.keys()
  return random.sample(containers_time.keys(), num_to_select)
