from twisted.words.protocols.irc import ERR_USERSDISABLED, ERR_NEEDMOREPARAMS


class Command(object):

    @staticmethod
    def can_user(server, client, username=None, ident=None, domain=None, realname=None):
        # Do nothing if the client has already registered
        if client.registered:
            pass
        # Request more parameters if username is null
        if not username:
            return ERR_NEEDMOREPARAMS
        # Users are disabled if they are in the restricted list
        if username in server.restricted_usernames:
            return ERR_USERSDISABLED

    @staticmethod
    def on_user(server, client, username, ident=None, domain=None, realname=None):
        client.username = username
        # If the user isn't registered, and they have a nickname and username, then register.
        # Note: register and authenticate are two different things.
        if client.nickname and not client.registered:
            client.hostmask = "%s!%s@%s" % (
                client.nickname, client.username, server.hostname)
            server.users[client.nickname] = client
            client.welcome()