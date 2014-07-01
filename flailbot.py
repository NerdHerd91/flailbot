# FlailBot - Provides on-demand flailing capabilities.

# Much of this structure is borrowed from the following example on the TwistedMatrix site.
# https://twistedmatrix.com/documents/12.0.0/core/howto/clients.html

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

# system imports
import sys

class FlailBot(irc.IRCClient):
    """A flailing IRC bot."""

    nickname = "FlailBot"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
    
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        if msg == ".flail":
            self.msg(channel, "FLAILLLLLLLLLL!!!")

class FlailBotFactory(protocol.ClientFactory):
    """A factory for FlailBots"""

    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        p = FlailBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

if __name__ == '__main__':
    # create factory protocol and application
    f = FlailBotFactory(sys.argv[1])

    # connect factory to this host and port
    reactor.connectTCP("irc.adelais.net", 6667, f)

    # run bot
    reactor.run()
