import socket
import logging
from twisted.internet import protocol
from betternet.network import Client

class TcpClient(protocol.Protocol, Client):

    def __init__(self, server):
        Client.__init__(self, server)
        self.server = server

    def dataReceived(self, data):
        self.receive(data)

    def send(self, line):
        self.transport.write(line.encode("utf8") + "\r\n")

    def connectionLost(self, reason="Connection lost"):
        protocol.Protocol.connectionLost(self, reason)
        self.server.dispatch(self, "quit", reason=reason)


class TcpFactory(protocol.Factory):

    def __init__(self, betternet):
        self.betternet = betternet
        self.log = logging.getLogger("TCP")

    def buildProtocol(self, addr):
        return TcpClient(self.betternet)