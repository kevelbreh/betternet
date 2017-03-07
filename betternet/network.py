import socket
from twisted.words.protocols.irc import parsemsg, CR, LF, ERR_NEEDMOREPARAMS, RPL_VERSION, RPL_ENDOFNAMES, RPL_NAMREPLY, \
    RPL_TOPIC, RPL_NOTOPIC



# https://docs.python.org/2/library/socket.html#socket.getfqdn
# https://docs.python.org/2/library/socket.html#socket.gethostbyaddr
def get_hostmask(ip):
    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(5)
    return socket.gethostbyaddr(ip)


class Client(object):

    def __init__(self, server):
        self._buffer = ""
        self._server = server
        self.registered = False
        self.authenticated = False
        self.away = False
        self.away_message = None
        self.away_timestamp = None
        self.nickname = None
        self.username = None
        self.hostmask = None
        self.channels = set()

    def send(self, line):
        pass

    def receive(self, data):
        lines = (self._buffer + data).split(LF)
        # Put the (possibly empty) element after the last LF back in the
        # buffer
        self._buffer = lines.pop()
        for line in lines:
            if len(line) <= 2:
                # This is a blank line, at best.
                continue
            if line[-1] == CR:
                line = line[:-1]
            prefix, command, params = parsemsg(line)
            # mIRC is a big pile of doo-doo
            command = command.lower()
            # DEBUG: log.msg( "%s %s %s" % (prefix, command, params))

            self._server.dispatch(self, command, *params)

    def visible_to(self):
        """
        Return a set of users clients that this user client is visible to. These are all the user clients
        in the same channels as this user client. No duplicates are returned.
        """
        visible_to = set()
        for channel in self.channels:
            visible_to = visible_to | channel.users
        return visible_to

    # gunslinger.shadowfire.org 433 * Russ :Nickname is already in use.
    # not sure what the star is about?
    def send_error(self, error, message):
        self.send(":%s %s %s :%s" % (self._server.hostname, error, self.nickname, message))

    def send_privmsg(self, prefix, target, message):
        self.send(":%s PRIVMSG %s :%s" % (prefix, target, message))

    def send_notice(self, prefix, target, message):
        self.send(":%s NOTICE %s :%s" % (prefix, target, message))

    def send_join(self, prefix, target):
        self.send(":%s JOIN %s" % (prefix, target))

    def send_part(self, prefix, target, reason):
        self.send(":%s PART %s :%s" % (prefix, target, reason))

    def send_quit(self, prefix, reason=None):
        self.send(":%s QUIT :%s" % (prefix, reason))

    def send_nick(self, prefix, nickname):
        self.send(":%s NICK :%s" % (prefix, nickname))

    def send_321(self):
        # <- :gunslinger.shadowfire.org 321 kevin Channel :Users  Name
        self.send(":%s 321 %s Channel :Users Name" % (self._server.hostname, self.nickname))

    def send_322(self, channel, users, topic):
        # <- :gunslinger.shadowfire.org 322 kevin #icfp 1 :
        self.send(":%s 322 %s %s %s :%s" % (
            self._server.hostname, self.nickname, channel, users, topic))

    def send_323(self):
        self.send(":%s 323 %s :End of /LIST" % (
            self._server.hostname, self.nickname))

    def send_331(self, channel, topic):
        self.send(":%s 331 %s :%s" % (self._server.hostname, channel, topic))

    def send_332(self, channel, topic):
        self.send(":%s 332 %s :%s" % (self._server.hostname, channel, topic))

    def send_333(self, channel, creator, timestamp):
        self.send(":%s 333 %s %s %s" % (self._server.hostname, channel, creator, timestamp))

    def send_366(self, channel):
        self.send(":%s 366 %s %s :End of /NAMES list" % (
            self._server.hostname, self.nickname, channel))

    # <- :gunslinger.shadowfire.org 353 kevin = ##### :@kevin!tester@354402E0.13456C05.E2DDCDED.IP
    def send_353(self, channel, users):
        if isinstance(users, list):
            users = " ".join(users)
        self.send(":%s 353 %s = %s :%s" % (
            self._server.hostname, self.nickname, channel, users))

    def send_numerical(self, prefix, numeric, params, args):
        if isinstance(params, list):
            params = " ".join(params)
        if isinstance(args, list):
            message = " ".join(args)
        self.send(":%s %s %s :%s" % (prefix, numeric, params, args))

    def send_pong(self, message):
        """
        Send a pong to the user client from the server.
        :param message: Argument that wil be sent back in the pong message
        """
        self.send(":%s PONG :%s" % (self._server.hostname, message))

    def topic(self, channel):
        # send the channel topic to the client
        server = self._server.hostname
        if channel.topic:
            self.send(":%s %s %s %s :%s" % (server, RPL_TOPIC, self.nickname, channel.name, channel.topic))
        else:
            self.send(":%s %s %s %s" % (server, RPL_NOTOPIC, self.nickname, channel.name))

    def names(self, channel):
        # send a names list of a channel to the client
        server = self._server.hostname
        for user in channel.users:
            self.send(":%s %s %s = %s :%s" % (
                server, RPL_NAMREPLY, self.nickname, channel.name, user.hostmask))
        self.send(":%s %s %s %s :%s" % (
            server, RPL_ENDOFNAMES, self.nickname, channel.name, "End of /NAMES list."))

    def welcome(self):
        """
        <- :gunslinger.shadowfire.org 002 kevin :Your host is gunslinger.shadowfire.org, running version Unreal3.2.10.3
        <- :gunslinger.shadowfire.org 003 kevin :This server was created Mon Jul 21 2014 at 22:19:56 SAST
        <- :gunslinger.shadowfire.org 004 kevin gunslinger.shadowfire.org Unreal3.2.10.3 iowghraAsORTVSxNCWqBzvdHtGpI lvhopsmntikrRcaqOALQbSeIKVfMCuzNTGjZ
        <- :gunslinger.shadowfire.org 005 kevin CMDS=KNOCK,MAP,DCCALLOW,USERIP,STARTTLS UHNAMES NAMESX SAFELIST HCN MAXCHANNELS=25 CHANLIMIT=#:25 MAXLIST=b:60,e:60,I:60 NICKLEN=30 CHANNELLEN=32 TOPICLEN=307 KICKLEN=307 AWAYLEN=307 :are supported by this server
        <- :gunslinger.shadowfire.org 005 kevin MAXTARGETS=20 WALLCHOPS WATCH=128 WATCHOPTS=A SILENCE=15 MODES=12 CHANTYPES=# PREFIX=(qaohv)~&@%+ CHANMODES=beI,kfL,lj,psmntirRcOAQKVCuzNSMTGZ NETWORK=ShadowFire CASEMAPPING=ascii EXTBAN=~,qjncrRaT ELIST=MNUCT :are supported by this server
        <- :gunslinger.shadowfire.org 005 kevin STATUSMSG=~&@%+ EXCEPTS INVEX :are supported by this server
        <- :gunslinger.shadowfire.org 251 kevin :There are 5 users and 349 invisible on 6 servers
        <- :gunslinger.shadowfire.org 252 kevin 14 :operator(s) online
        <- :gunslinger.shadowfire.org 253 kevin 2 :unknown connection(s)
        <- :gunslinger.shadowfire.org 254 kevin 197 :channels formed
        <- :gunslinger.shadowfire.org 255 kevin :I have 123 clients and 0 servers
        <- :gunslinger.shadowfire.org 265 kevin 123 335 :Current local users 123, max 335
        <- :gunslinger.shadowfire.org 266 kevin 354 3432 :Current global users 354, max 3432
        <- :gunslinger.shadowfire.org 375 kevin :- gunslinger.shadowfire.org Message of the Day -
        <- :gunslinger.shadowfire.org 372 kevin :- 8/4/2015 13:05
        :return:
        """
        self.send(":%s 001 %s :Welcome to the %s IRC Network %s" % (
            self._server.hostname, self.nickname, self._server.display_name, self.hostmask))