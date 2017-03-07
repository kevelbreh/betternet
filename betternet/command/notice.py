from twisted.words.protocols.irc import ERR_NORECIPIENT, ERR_NOTEXTTOSEND, ERR_NOSUCHNICK

class Command(object):
    """
    The NOTICE command is used similarly to PRIVMSG.  The difference
    between NOTICE and PRIVMSG is that automatic replies MUST NEVER be
    sent in response to a NOTICE message.  This rule applies to servers

    too - they MUST NOT send any error reply back to the client on
    receipt of a notice.  The object of this rule is to avoid loops
    between clients automatically sending something in response to
    something it received.

    This command is available to services as well as users.

    This is typically used by services, and automatons (clients with
    either an AI or other interactive program controlling their actions).

    See PRIVMSG for more details on replies and examples.
    """

    @staticmethod
    def can_notice(server, client, target=None, message=None):
        if not target:
            return ERR_NORECIPIENT
        if not message:
            return ERR_NOTEXTTOSEND
        # Check if user exists.
        entity = server.get_user(target)
        if entity:
            return 0
        # Check if channel exists.
        entity = server.get_channel(target)
        if entity:
            return 0
        return ERR_NOSUCHNICK

    @staticmethod
    def on_notice(server, client, target, message):
        user = server.get_user(target)
        if user:
            user.send_notice(client.hostmask, user.nickname, message)
            return
        channel = server.get_channel(target)
        for user in channel.users:
            if user == client:
                continue
            user.send_notice(client.hostmask, target, message)