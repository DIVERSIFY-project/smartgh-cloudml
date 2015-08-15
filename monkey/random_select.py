import numpy
import random
from monkeylib import resolve_func

def random_select(containers_time, number):
  if len(containers_time) == 0:
    return []
  func = resolve_func(number)


  num_to_select = func()
  if (type(num_to_select) is list) and len(num_to_select)>0:
    num_to_select = num_to_select[0]
  num_to_select = int(num_to_select)
  if num_to_select >= len(containers_time.keys()):
    return containers_time.keys()
  return random.sample(containers_time.keys(), num_to_select)
