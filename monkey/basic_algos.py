import numpy
import random
from monkeylib import resolve_func

def random_select(samples, number):
  if len(samples) == 0:
    return []
  func = resolve_func(number, samples)


  num_to_select = func()
  if (type(num_to_select) is list) and len(num_to_select)>0:
    num_to_select = num_to_select[0]
  num_to_select = int(num_to_select)
  if num_to_select >= len(samples.keys()):
    return samples.keys()
  return random.sample(samples.keys(), num_to_select)

expected_age = dict()
def by_age(samples, lifespan):
  global expected_age
  func = resolve_func(lifespan)
  for c in samples:
    if samples[c] == 0:
      expected_age[c] = int(func())
  return [ x for (x,y) in samples.iteritems() if y >= expected_age[x]] 

def by_reliability(samples, reliability):
  func = resolve_func(reliability, samples)
  result = []  
  for c in samples:
    age = samples[c]
    r = func(age)
    if random.random() > r:
      result.append(c)
  return result
  
def simple_poisson(samples, single_rate):
  return random_select(samples, {'module':'numpy.random', 'function':'poisson', 'lam':single_rate*len(samples)})

def two_param_weibull(shape, scale):
  return numpy.random.weibull(shape) * scale

def weibull_reliability_age(age, shape, scale):
  return numpy.exp(-(float(age) / scale)**shape)
