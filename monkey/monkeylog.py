import yaml

class Logger:
  def __init__(self, name):
    self.filepath = "logs/%s.log" % name
    f = open(self.filepath, 'w')
    f.close()

    self.current_item = {}

  def new_cycle(self,cycle):
    self.current_item.clear()
    self.current_item['cycle'] = cycle

  def log(self, key, value):
    self.current_item[key] = value

  def flush(self):
    f = open(self.filepath, 'a')
    f.write("---\n")
    f.write(yaml.dump(self.current_item))
    f.close()
