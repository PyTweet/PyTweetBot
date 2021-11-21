import discord
import aiohttp
from discord.ext import commands

class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_webhook = self.bot.log_webook

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            embed = {
                "color": 0x5865f2,
                "description": f"""
                Message sent in {message.channel.mention}
                Author: {message.author.mention}
                Content: {message.content}
                Sent {discord.utils.format_dt(message.created_at, style = "R")}
                [Jump to message]({message.jump_url})
                """
            }

            payload = {
                "embeds": [
                    embed
                ]
            }

            async with aiohttp.ClientSession() as session:
                await session.post(
                    url = self.log_webhook,
                    json = payload
                )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot and not after.author.bot:
            embed = {
                "color": 0x5865f2,
                "description": f"""
                Message edited in {before.channel.mention}
                Author: {before.author.mention}
                **Before:** {before.content}
                at {discord.utils.format_dt(before.created_at)}
                **After:** {after.content}
                Edited {discord.utils.format_dt(discord.utils.utcnow())}
                [Jump to message]({before.jump_url})
                """
            }

            payload = {
                "embeds": [
                    embed
                ]
            }

            async with aiohttp.ClientSession() as session:
                await session.post(
                    url = self.log_webhook,
                    json = payload
                )

def setup(bot):
    bot.add_cog(Log(bot))