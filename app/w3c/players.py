from twitchio.ext import commands
from w3c.player import Player

class Players(dict):
    def __init__(self, testing = True, **config):
        self.testing = testing
        self.load_players()

    async def add_player(self, twitch_name, battletag: str):
        player = Player(twitch_name, battletag)
        stats = player.get_stats()
        assert stats
        self[twitch_name] = player
        self.save()

    def remove_player(self, twitch_name):
        if self.get(twitch_name):
            del self[twitch_name]
            self.save()
            return True
        return False

    async def find_player_match(self, ctx: commands.Context):
        if self.get(ctx.channel.name):
            player: Player = self[ctx.channel.name]
            match = player.get_current_match()
            if match:
                await ctx.channel.send(match.describe_teams(player.bnet))
            else:
                await ctx.channel.send("not currently in a match")
        else:
            print(f"No player registered for this channel: {ctx.channel.name}")

    def load_players(self):
        if self.testing:
            return
        with open("players.save", "r") as f:
            for p in f.readlines():
                twitch_channel, bnet_id = p.split(":")
                self[twitch_channel] = Player(twitch_channel, bnet_id)

    def save(self):
        # if self.testing:
        #     return
        with open("players.save", "w") as f:
            f.writelines([f"{k}:{v.bnet}" for k, v in self.items()])
