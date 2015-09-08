import yaml

metas = None

def read_metas(path):
  meta_file = open(path, 'r');
  global metas
  metas = yaml.load(meta_file)


