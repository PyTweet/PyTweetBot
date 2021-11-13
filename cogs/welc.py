import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot, name = "Auto Responses"):
        self.bot = bot

def setup(bot):
    bot.add_cog(Welcome(bot))