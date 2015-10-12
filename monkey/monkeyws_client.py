import json

from ws4py.client.threadedclient import WebSocketClient

tick = False

clients = set()
server = None


class GHClient(WebSocketClient):
    def opened(self):
        print "GHClient opened up"

    def closed(self, code, reason=None):
        print "Closed down ", code, reason

    def received_message(self, message):
        print "Received %s" % message
        global tick
        parsed_message = json.loads(str(message))
        tick = True
        print "Tick %d" % parsed_message["tick"]

    def push(self, data):
        self.send(data)

def connect(ipaddress):
	print "Starting client"
	print 'ws://'+ipaddress+':8099/'
	ws = GHClient('ws://'+ipaddress+':8099/')
	print "Waiting for server..."
	ws.connect()
	print "Connected"