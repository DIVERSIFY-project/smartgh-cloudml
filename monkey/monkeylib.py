import inspect
from plumbum import local
import yaml

docker_ps_a = local["docker"]["ps"]["-a"]
grep = local["grep"]
static_metas = None

def get_static_metas():
  global static_metas
  return static_metas

class ContainerMeta:
  def __init__(self, line):
    print line
    items = line.split()
    self.id = items[0]
    self.image = items[1]
    self.name = items[-1]

container_meta = dict()

def add_to_container_meta(id):
  if id in container_meta:
    return  
  line = (docker_ps_a | grep[id]) ()
  container = ContainerMeta(line)
  container_meta[id] = container

def check_meta(metadict):
  for k in metadict:
    v = metadict[k]
    for mkeyword in ['services', 'clients']:
      try:
        if not(type(v[mkeyword]) is list):
          raise Exception('Not a list')
      except Exception as e:
        raise Exception(e, 'Container meta file format error at %s/%s' % (k, mkeyword))

def init_static_meta(meta_file_path):
  global static_metas
  meta_file = file(meta_file_path, 'r')
  static_metas = yaml.load(meta_file)
  check_meta(static_metas)



def container_name(id):
  return container_meta[id].name

def container_names(ids):
  return [container_meta[id].name.encode('ascii') for id in ids]

def resolve_func(func_config, samples = None):
  if not type(func_config) is dict:
    return lambda : func_config

  config = func_config.copy()
  exec 'import %s' % config['module'] in globals(), locals()
  func = eval('%s.%s' %(config['module'], config['function']))
  del config['module']
  del config['function']

  for key in config:
    v = config[key]
    if type(v) is str and v.strip().startswith('('):
      config[key] = eval(v.strip())  
      #print config[key]

  reserve_first = config.pop('reserve_first_arg', False)
  if reserve_first:
    return lambda arg0 : func(arg0, **config)
  else:
    return lambda : func(**config)


