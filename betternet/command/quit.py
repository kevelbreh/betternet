

class Command(object):

    @staticmethod
    def can_quit(server, client, reason=None):
        return 0

    @staticmethod
    def on_quit(server, client, reason=None):
        if client.nickname not in server.users.keys():
            # FIXME: delete user from reactor/factory also
            print "not in server.users"
            return
        # Set an empty reason else None is written out as text.
        if not reason:
            reason = ""
        # Inform the visible clients.
        users = client.visible_to()
        for user in users:
            user.send_quit(client.hostmask, reason)
        # Remove the user from channels and the server.
        for channel in client.channels:
            channel.users.remove(client)
        del server.users[client.nickname]