# will update later :))

import discord, asyncio, time
from discord.ext import commands, tasks

class BumpReminder(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bump_reminder.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.channel.id == 872356768464912494:return
        if not message.content == "!d bump":return
        def check(msg: discord.Message):
            if not msg.author.id == 302050872383242240:return False
            for embed in msg.embeds:
                if "Bump done!" in embed.description:
                    self.bot.loop.create_task(msg.channel.send("I will remind you in <#858312394756980781> in 2 hours!"))
                    self.bot.last_bump = time.time()
            return True
        try:await self.bot.wait_for("message", check = check, timeout = 10)
        except:pass

    @tasks.loop(minutes = 20)
    async def bump_reminder(self):
        bot = self.bot
        last_bump: float = bot.last_bump
        if last_bump:
            if (time.time() - last_bump) > 7200:
                await bot.get_channel(858312394756980781).send("Time to bump! Type !d bump in <#872356768464912494>!")

    @bump_reminder.before_loop
    async def before_bump_reminder(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(BumpReminder(bot))
