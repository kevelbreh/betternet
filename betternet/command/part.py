from twisted.words.protocols.irc import ERR_NEEDMOREPARAMS, ERR_NOSUCHCHANNEL, ERR_NOTONCHANNEL


class Command(object):
    """
    The PART command causes the user sending the message to be removed
    from the list of active members for all given channels listed in the
    parameter string.  If a "Part Message" is given, this will be sent
    instead of the default message, the nickname.  This request is always
    granted by the server.

    Servers MUST be able to parse arguments in the form of a list of
    target, but SHOULD NOT use lists when sending PART messages to
    clients.

    Numeric Replies:

           ERR_NEEDMOREPARAMS              ERR_NOSUCHCHANNEL
           ERR_NOTONCHANNEL

    Examples:

    PART #twilight_zone             ; Command to leave channel
                                   "#twilight_zone"

    PART #oz-ops,&group5            ; Command to leave both channels
                                   "&group5" and "#oz-ops".

    :WiZ!jto@tolsun.oulu.fi PART #playzone :I lost
                                   ; User WiZ leaving channel
                                   "#playzone" with the message "I
                                   lost".

        #derp No such channel
        #shadowfire You're not on that channel
    """

    @staticmethod
    def can_part(server, client, channel=None, argument=None):
        # Check if channel
        if not channel:
            return ERR_NEEDMOREPARAMS
        chan = server.get_channel(channel)
        # Check if channel exists
        if not chan:
            return ERR_NOSUCHCHANNEL
        # Check for valid channel key
        if client not in chan.users:
            return ERR_NOTONCHANNEL

    @staticmethod
    def on_part(server, client, channel, reason=None):
        if not reason:
            reason = client.nickname
        chan = server.get_channel(channel)
        # inform other channel users.
        users = chan.users
        for user in users:
            user.send_part(client.hostmask, chan.name, reason)
        # bind channel and client
        chan.users.remove(client)
        client.channels.remove(chan)