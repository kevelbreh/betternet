from twisted.words.protocols.irc import ERR_NEEDMOREPARAMS, ERR_NOSUCHCHANNEL, ERR_BADCHANNELKEY


class Command(object):
    """
    The MODE command is provided so that users may query and change the
    characteristics of a channel.  For more details on available modes
    and their uses, see "Internet Relay Chat: Channel Management" [IRC-
    CHAN].  Note that there is a maximum limit of three (3) changes per
    command for modes that take a parameter.

    Numeric Replies:

           ERR_NEEDMOREPARAMS              ERR_KEYSET
           ERR_NOCHANMODES                 ERR_CHANOPRIVSNEEDED
           ERR_USERNOTINCHANNEL            ERR_UNKNOWNMODE
           RPL_CHANNELMODEIS
           RPL_BANLIST                     RPL_ENDOFBANLIST
           RPL_EXCEPTLIST                  RPL_ENDOFEXCEPTLIST
           RPL_INVITELIST                  RPL_ENDOFINVITELIST
           RPL_UNIQOPIS

    The following examples are given to help understanding the syntax of
    the MODE command, but refer to modes defined in "Internet Relay Chat:
    Channel Management" [IRC-CHAN].

    Examples:

    MODE #Finnish +imI *!*@*.fi     ; Command to make #Finnish channel
                                   moderated and 'invite-only' with user
                                   with a hostname matching *.fi
                                   automatically invited.

    MODE #Finnish +o Kilroy         ; Command to give 'chanop' privileges
                                   to Kilroy on channel #Finnish.

    MODE #Finnish +v Wiz            ; Command to allow WiZ to speak on
                                   #Finnish.

    MODE #Fins -s                   ; Command to remove 'secret' flag
                                   from channel #Fins.

    MODE #42 +k oulu                ; Command to set the channel key to
                                   "oulu".

    MODE #42 -k oulu                ; Command to remove the "oulu"
                                   channel key on channel "#42".

    MODE #eu-opers +l 10            ; Command to set the limit for the
                                   number of users on channel
                                   "#eu-opers" to 10.

    :WiZ!jto@tolsun.oulu.fi MODE #eu-opers -l
                                   ; User "WiZ" removing the limit for
                                   the number of users on channel "#eu-
                                   opers".

    MODE &oulu +b                   ; Command to list ban masks set for
                                   the channel "&oulu".

    MODE &oulu +b *!*@*             ; Command to prevent all users from
                                   joining.

    MODE &oulu +b *!*@*.edu +e *!*@*.bu.edu
                                   ; Command to prevent any user from a
                                   hostname matching *.edu from joining,
                                   except if matching *.bu.edu

    MODE #bu +be *!*@*.edu *!*@*.bu.edu
                                   ; Comment to prevent any user from a
                                   hostname matching *.edu from joining,
                                   except if matching *.bu.edu

    MODE #meditation e              ; Command to list exception masks set
                                   for the channel "#meditation".

    MODE #meditation I              ; Command to list invitations masks
                                   set for the channel "#meditation".

    MODE !12345ircd O               ; Command to ask who the channel
                                   creator for "!12345ircd" is
    """

    @staticmethod
    def can_mode(server, client, channel=None, modes=None, params=None):
        # Check if channel
        if not channel:
            return ERR_NEEDMOREPARAMS
        chan = server.get_channel(channel)
        # Check if channel exists
        if not chan:
            return ERR_NOSUCHCHANNEL

    @staticmethod
    def on_mode(server, client, channel=None, key=None):
        chan = server.get_channel(channel)
