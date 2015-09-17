from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import thread
import time

tick = False

clients = set()
server = None

class SimpleEcho(WebSocket):


  def received_message(self, message):
        # echo message back to client
    global tick
    if str(message).strip().lower() == "tick":
      tick = True
#    for i in self.pool:
#      self.send(i, message.is_text)
        
  def opened(self):
    global clients
    clients.add(self)
    print "%s connected" % self

  def push(self, data):
    self.send(data)

def run_server(server):
  #try:
  server.serve_forever()
  #except:
  #  pass

def start_server():
  global server
  server = make_server('', 8099, server_class=WSGIServer,
                     handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls=SimpleEcho))
  server.initialize_websockets_manager()
  #print server
  
  thread.start_new_thread(run_server, (server,))
  #server.serve_forever()

def stop_server():
  global server
  if server:
    server.stop()

def push(data):
  for c in clients:
    c.push(data)

#start_server()
#while 1:
#  time.sleep(1)
#  print "hey"

