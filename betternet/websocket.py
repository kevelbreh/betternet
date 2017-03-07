import logging
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from betternet.network import Client


class WsClient(WebSocketServerProtocol, Client):

    def __init__(self):
        Client.__init__(self, None)
        self.server = None

    def onOpen(self):
        self.server = self.factory.betternet
        self._server = self.server

    def connectionLost(self, reason="Connection lost"):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.server.dispatch(self, "quit", reason=reason)

    def send(self, line):
        self.sendMessage("%s\r\n" % line.encode("utf8"), isBinary=False)

    # noinspection PyPep8Naming
    def onMessage(self, payload, isBinary):
        print "get line: ", payload
        if not isBinary:
            self.receive(payload.decode('utf8'))


class WsFactory(WebSocketServerFactory):

    protocol = WsClient

    def __init__(self, betternet):
        WebSocketServerFactory.__init__(self, url='ws://localhost:8889')
        self.betternet = betternet
        self.log = logging.getLogger("WS")