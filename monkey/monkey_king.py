from kazoo.client import KazooClient
import sys
if '-z' in sys.argv:
  zookeeper_addr = sys.argv[sys.argv.index('-z')+1]
  zookeeper = KazooClient(hosts=zookeeper_addr)
  zookeeper.start()
else:
  print "no zookeeper, use -z host:port"
  exit()

for s in zookeeper.get_children("/monkey"):
   zookeeper.set("/monkey/%s/tick"%s, b't')

zookeeper.stop()
