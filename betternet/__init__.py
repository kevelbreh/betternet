import logging
import importlib
from twisted.internet import reactor

from betternet.websocket import WsFactory
from betternet.tcp import TcpFactory
from betternet.util import CaseInsensitiveDict


logging.basicConfig(file='betternet.log', level=logging.DEBUG)


class Channel(object):

    def __init__(self, name, key=None):
        self.name = name
        self.key = key
        self.users = set()
        self.topic = None
        self.topic_creator = None
        self.topic_timestamp = None


class Betternet(object):

    commands = set()

    users = CaseInsensitiveDict()
    channels = CaseInsensitiveDict()

    restricted_nicknames = []
    restricted_usernames = []
    channel_prefixes = ['#']

    display_name = "Kevelbreh"
    hostname = "chat.kevelbreh.co.za"



    def __init__(self):
        self.log = logging.getLogger("core")
        self.__init__modules()
        self.__init__commands()
        self.__init__servers()

    def __init__modules(self):
        self.channels['#chat'] = Channel("#chat")
        pass

    def __init__servers(self):
        reactor.listenTCP(8888, TcpFactory(self))
        reactor.listenTCP(8889, WsFactory(self))
        pass

    def __init__commands(self):
        temp = ['ping', 'user', 'nick', 'mode', 'join', 'part', 'quit', 'privmsg', 'notice', 'names', 'list', 'topic']
        for name in temp:
            try:
                module = importlib.import_module('betternet.command.%s' % name)
                klass = getattr(module, 'Command')
            except Exception, e:
                self.log.warning(u"Couldn't import betternet.command.%s: %s", name, unicode(e))
                continue
            self.commands.add(klass())

    def start(self):
        self.log.info(u"Running reactor.")
        reactor.run()

    def dispatch(self, client, cmd, *args, **kwargs):
        print "handling: ", cmd
        for command in self.commands:
            can_method = getattr(command, "can_%s" % cmd, None)
            if can_method is None:
                continue
            error = can_method(self, client, *args, **kwargs)
            if error and error != 0:
                client.send_error(error, "error")
                return  # and send the error
        for command in self.commands:
            on_method = getattr(command, "on_%s" % cmd, None)
            if on_method is None:
                continue
            on_method(self, client, *args, **kwargs)

    def get_channel(self, channel):
        return self.channels.get(channel)

    def get_user(self, nickname):
        try:
            return self.users[nickname]
        except KeyError:
            self.log.warning(u"Returning a null client on get_user(%s)", nickname)
            return None


if __name__ == "__main__":
    application = Betternet()
    application.start()