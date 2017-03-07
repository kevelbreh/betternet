
class Command(object):
    """
    The list command is used to list channels and their topics.  If the
    <channel> parameter is used, only the status of that channel is
    displayed.

    If the <target> parameter is specified, the request is forwarded to
    that server which will generate the reply.

    Wildcards are allowed in the <target> parameter.

    Numeric Replies:

           ERR_TOOMANYMATCHES              ERR_NOSUCHSERVER
           RPL_LIST                        RPL_LISTEND

    Examples:

    LIST                            ; Command to list all channels.

    LIST #twilight_zone,#42         ; Command to list channels
                                   #twilight_zone and #42
    """

    @staticmethod
    def can_list(server, client, target=None):
        return 0

    @staticmethod
    def on_list(server, client, target=None):
        # start of list and format
        client.send_321()
        for chan, channel in server.channels.iteritems():
            # each channel item with its name, user count and topic
            client.send_322(channel.name, len(channel.users), channel.topic)
        # end of list.
        client.send_323()