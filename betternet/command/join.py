from twisted.words.protocols.irc import ERR_NEEDMOREPARAMS, ERR_NOSUCHCHANNEL, ERR_BADCHANNELKEY


class Command(object):
    """
    The JOIN command is used by a user to request to start listening to
    the specific channel.  Servers MUST be able to parse arguments in the
    form of a list of target, but SHOULD NOT use lists when sending JOIN
    messages to clients.

    Once a user has joined a channel, he receives information about
    all commands his server receives affecting the channel.  This
    includes JOIN, MODE, KICK, PART, QUIT and of course PRIVMSG/NOTICE.
    This allows channel members to keep track of the other channel
    members, as well as channel modes.

    If a JOIN is successful, the user receives a JOIN message as
    confirmation and is then sent the channel's topic (using RPL_TOPIC) and
    the list of users who are on the channel (using RPL_NAMREPLY), which
    MUST include the user joining.

    Note that this message accepts a special argument ("0"), which is
    a special request to leave all channels the user is currently a member
    of.  The server will process this message as if the user had sent
    a PART command (See Section 3.2.2) for each channel he is a member
    of.

    Numeric Replies:

           ERR_NEEDMOREPARAMS              ERR_BANNEDFROMCHAN
           ERR_INVITEONLYCHAN              ERR_BADCHANNELKEY
           ERR_CHANNELISFULL               ERR_BADCHANMASK
           ERR_NOSUCHCHANNEL               ERR_TOOMANYCHANNELS
           ERR_TOOMANYTARGETS              ERR_UNAVAILRESOURCE
           RPL_TOPIC

    Examples:

    JOIN #foobar                    ; Command to join channel #foobar.

    JOIN &foo fubar                 ; Command to join channel &foo using
                                   key "fubar".

    JOIN #foo,&bar fubar            ; Command to join channel #foo using
                                   key "fubar" and &bar using no key.

    JOIN #foo,#bar fubar,foobar     ; Command to join channel #foo using
                                   key "fubar", and channel #bar using
                                   key "foobar".

    JOIN #foo,#bar                  ; Command to join channels #foo and
                                   #bar.

    JOIN 0                          ; Leave all currently joined
                                   channels.

    :WiZ!jto@tolsun.oulu.fi JOIN #Twilight_zone ; JOIN message from WiZ
                                   on channel #Twilight_zone
    """

    @staticmethod
    def can_join(server, client, channel=None, key=None):
        # Check if channel
        if not channel:
            return ERR_NEEDMOREPARAMS
        chan = server.get_channel(channel)
        # Check if channel exists
        if not chan:
            return ERR_NOSUCHCHANNEL
        # Check for valid channel key
        if key and chan.key != key:
            return ERR_BADCHANNELKEY

    @staticmethod
    def on_join(server, client, channel, key=None):
        chan = server.get_channel(channel)
        # inform other channel users.
        users = chan.users
        for user in users:
            user.send_join(client.hostmask, chan.name)
        # bind channel and client
        chan.users.add(client)
        client.channels.add(chan)
        client.send_join(client.hostmask, chan.name)
        # send topic details to the user
        if chan.topic:
            client.send_332(chan.name, chan.topic)
            client.send_333(chan.name, chan.topic_creator, chan.topic_timestamp)
        else:
            client.send_331(chan.name, "No topic is set")
        # send user list to the user
        client.send_366(chan.name)
        server.dispatch(client, "names", channel)
