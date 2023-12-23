import twitchio
from twitchio.ext import commands
from cogs.warcraft import WarcraftCog
from tools.config import config
from w3c.players import Players

class TwitchBot(commands.Bot, twitchio.Client):

    players: Players
    def __init__(self):
        super().__init__(
            prefix='?', token=config['credential']['access_token']
        )
        self.players = Players()
        self.add_cog(WarcraftCog(self.nick, self.players, self))
        self.run()

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in - Ready')
        await self.join_channels(
            [*self.players.keys(), self.nick]
        )

    async def event_join(self, *args):
        print(f"Joined server {args}")

    async def event_part(self, *args):
        print(f"Part server {args}")

if __name__ == '__main__':
    bot = TwitchBot()
    bot.run()
