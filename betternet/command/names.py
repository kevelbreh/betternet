
class Command(object):
    """
    By using the NAMES command, a user can list all nicknames that are
    visible to him. For more details on what is visible and what is not,
    see "Internet Relay Chat: Channel Management" [IRC-CHAN].  The
    <channel> parameter specifies which channel(s) to return information
    about.  There is no error reply for bad channel names.

    If no <channel> parameter is given, a list of all channels and their
    occupants is returned.  At the end of this list, a list of users who
    are visible but either not on any channel or not on a visible channel
    are listed as being on `channel' "*".

    If the <target> parameter is specified, the request is forwarded to
    that server which will generate the reply.

    Wildcards are allowed in the <target> parameter.

    Numerics:

           ERR_TOOMANYMATCHES              ERR_NOSUCHSERVER
           RPL_NAMREPLY                    RPL_ENDOFNAMES

    Examples:

    NAMES #twilight_zone,#42        ; Command to list visible users on
                                   #twilight_zone and #42

    NAMES                           ; Command to list all visible
                                   channels and users
    """

    @staticmethod
    def can_names(server, client, channel=None):
        pass


    """
    <- :gunslinger.shadowfire.org 353 kevin = #gopugs :kevin Sven fragtion FlaMeBeRg @GameBot ~@Russ!
<- :gunslinger.shadowfire.org 353 kevin = #gopugs :Lithium!~AndrewMoh@SF-3740E9DA.andrewmohawk.com Webtricity!web@staff.shadowfire.org
    """
    @staticmethod
    def on_names(server, client, channel=None):
        chan = server.get_channel(channel)
        # Send end of list
        if not channel or not chan:
            client.send_366("*")
            return
        # Send channel with empty users.
        if client not in chan.users:
            client.send_353(channel, [])
            client.send_366(channel)
            return
        # Send proper names list now. Split into lists of max 6 users
        users = chan.users
        temp = []
        for user in users:
            temp.append(user.hostmask)
            if len(temp) == 6:
                client.send_353(channel, temp)
                temp = []
        client.send_353(channel, temp)
        client.send_366(channel)
