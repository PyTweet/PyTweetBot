import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.name = "Welcome Handler"


def setup(bot):
    bot.add_cog(Welcome(bot))
