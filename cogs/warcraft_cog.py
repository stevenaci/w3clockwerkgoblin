from twitchio.ext import commands
from twitchio import Channel
from tools.toon import ToonString
from tools.error import catch_all_exceptions
from w3c.players import Players

class WarcraftCog(commands.Cog):

    server_channel: str
    players: Players

    def __init__(self, players: Players, bot: commands.bot):
        self.players = players
        self.bot = bot
    
    def set_server_channel(self, channel: str):
        print(f"Setting Clockwerk Server as channel: {channel}")
        self.server_channel =  channel

    def is_server_channel(self, ctx: commands.Context):
        return ctx.channel.name == self.server_channel
    
    async def sendToon(self, ctx: commands.Context, message: str):
        await ctx.channel.send(ToonString(message))

    @commands.command()
    async def oppo(self, ctx: commands.Context):
        """ Returns: Info for the player's current match"""
        try:
            match = await self.players.find_player_match(ctx.author.name)
            await self.sendToon(ctx, match.describe())
        except Exception as e: # Match wasn't found or something else bad happened.
            print(e)
            await self.sendToon(ctx, "Player is not in a ladder match")

    @commands.command()
    async def join(self, ctx: commands.Context):
        """ Command to join the Clockwerk Network, 
            or to change the player associated with your account.
            If the message is sent
        """
        if self.is_server_channel(ctx) or ctx.message.author.is_broadcaster:
            try:
                battletag = ctx.message.content.split(" ")[1]
            except:
                await self.sendToon(ctx, "Specify A BattleTag :OVVVO:!")
                return
            try:
                await self.players.add_player(ctx.message.author.name, battletag)
                await self.sendToon(ctx, f"Battletag {battletag} was assigned to channel {ctx.message.author.name}")
                if self.players.get(ctx.message.author.name):
                    await self.bot.join_channels([ctx.message.author.name])
            except:
                await self.sendToon(ctx, "Couldn't find that battletag on w3c network.")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        if self.is_server_channel(ctx) or ctx.message.author.is_broadcaster:
            if self.players.remove_player(ctx.author.name):
                await ctx.channel.send(f" {ctx.author.name}, your channel has been removed!")
                await self.bot.part_channels([ctx.author.name])
            else:
                await ctx.channel.send(f"No player currently assigned to the channel: {ctx.author.name}")

    @commands.command()
    async def player_status(self, ctx: commands.Context):
        await ctx.channel.send(f"{self.players[ctx.channel.name]}")
