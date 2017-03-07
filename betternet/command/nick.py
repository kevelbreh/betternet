from twisted.words.protocols.irc import ERR_NONICKNAMEGIVEN, ERR_NICKNAMEINUSE, ERR_RESTRICTED, ERR_ERRONEUSNICKNAME


class Command(object):

    @staticmethod
    def can_nick(server, client, nickname=None):
        # Check to make sure there are enough parameters
        if not nickname:
            return ERR_NONICKNAMEGIVEN
        # Check to see if this nickname is being used
        user = server.get_user(nickname)
        if user and user != client:
            return ERR_NICKNAMEINUSE
        # Check nickname restrictions
        if nickname in server.restricted_nicknames:
            return ERR_RESTRICTED

    @staticmethod
    def on_nick(server, client, nickname):
        # If not registered, set the nick and hostmask then welcome the user to the server.
        if not client.registered:
            client.nickname = nickname
            client.hostmask = "%s!%s@%s" % (
                client.nickname, client.username, server.hostname)
            if not client.username:
                return
            server.users[client.nickname] = client
            client.welcome()
            return
        # If the user has already been registered with the server, just notify all his visible peers that
        # his nickname has changed.
        for other_client in client.visible_to():
            other_client.nick(client.hostmask, nickname)
        client.send_nick(client.hostmask, nickname)
        client.nickname = nickname
        client.hostmask = "%s!%s@%s" % (
            client.nickname, client.username, server.hostname)

