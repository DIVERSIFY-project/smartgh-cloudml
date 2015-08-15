import inspect


def resolve_func(func_config):
  if not type(func_config) is dict:
    return lambda : func_config

  config = func_config.copy()
  exec 'import %s' % config['module'] in globals(), locals()
  func = eval('%s.%s' %(config['module'], config['function']))
  del config['module']
  del config['function']
  reserve_first = config.pop('reserve_first_arg', False)
  if reserve_first:
    return lambda arg0 : func(arg0, **config)
  else:
    return lambda : func(**config)


