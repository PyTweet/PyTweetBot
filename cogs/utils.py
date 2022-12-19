import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="snipe")
    async def del_snipe(self, ctx: commands.Context):
        if len(self.bot.del_snipe) == 0:
            snipeEm: discord.Embed = discord.Embed(
                title="No messages have been deleted since bot start!",
                colour=discord.Colour.red(),
            )
            return await ctx.send(embed=snipeEm)

        snipeList = [
            f"**Message Sent in {msg.channel.mention} by {msg.author.mention}**:\n{msg.content}"
            for msg in self.bot.del_snipe
        ]
        snipeStr = "\n".join(snipeList)
        snipeEm: discord.Embed = discord.Embed(
            title="Deleted messages!",
            description=f"This are the previous {len(snipeList)} messages deleted in this server!\n\n{snipeStr}",
        )
        await ctx.send(embed=snipeEm)


def setup(bot):
    bot.add_cog(Utils(bot))
