import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr

class FlailBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self,[(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return
    
    def do_command(self, e, cmd):
        nick = e.source.nick
        c.self.connection

        if cmd == "flailbot disconnect":
            self.disconnect()
        elif cmd == "flailbot die":
            self.die()
        elif cmd == "flailbot flail":
            c.notice(nick, "flailllllllllll!!!")

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: flailbot <server[:port]> <channel> <nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = FlailBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
