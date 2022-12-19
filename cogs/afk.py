import typing
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
import humanize


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._afk_peeps = {}

    async def update_cache(self) -> typing.Dict[int, typing.Dict[str, typing.Any]]:
        async for m in self.bot.afk.find():
            self._afk_peeps[m["_id"]] = m
        return self._afk_peeps

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            aid = message.author.id
            c = self._afk_peeps.get(aid)
            if c:
                await message.reply(
                    f"Welcome back {message.author.name}! I have removed your afk!"
                )
                await self.bot.afk.delete_one({"_id": message.author.id})
                self._afk_peeps.pop(aid, None)
                if isinstance(message.author.nick, str):
                    try:
                        await message.author.edit(
                            nick=message.author.nick.replace("[AFK]", "")
                        )
                    except commands.BotMissingPermissions:
                        pass
            else:
                for member in message.mentions:
                    check = self._afk_peeps.get(member.id)
                    if check is not None:
                        await message.reply(
                            f"**{member}** is AFK - {check['message']} - {humanize.naturaltime(check['start'])}"
                        )

    @commands.group(name="afk", invoke_without_command=True)
    async def afk(self, ctx, *, message: str = "AFK"):
        aid = ctx.author.id
        u = self._afk_peeps.get(aid)
        if u is None:
            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
            except:
                pass
            await ctx.reply(f"Set your AFK status - **{message}**")
            await asyncio.sleep(10)
            data = {"_id": aid, "message": message, "start": discord.utils.utcnow()}
            self._afk_peeps[aid] = data
            try:
                await self.bot.afk.insert_one(data)
            except:
                await self.bot.afk.update_one({"_id": ctx.author.id}, {"$set": data})

    @afk.command(name="remove")
    @has_permissions(administrator=True)
    async def remove(self, ctx, member: discord.Member):
        u = self._afk_peeps.get(member.id)
        if u is None:
            return await ctx.send(f"{member} is not afk!")

        await self.bot.afk.delete_one(u)
        self._afk_peeps.pop(u, None)
        if isinstance(member.nick, str):
            if member.nick.startswith("[AFK]"):
                try:
                    await member.edit(nick=f"{member.nick[5:]}")
                except commands.BotMissingPermissions:
                    pass
        await ctx.send(f"Removed **{member.display_name}**'s AFK!")


def setup(bot):
    bot.add_cog(Afk(bot))
