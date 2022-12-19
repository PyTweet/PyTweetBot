import discord
from discord.ext import commands
import os
from motor.motor_asyncio import AsyncIOMotorClient
import webserver
import aiohttp
import traceback
import asyncio

class Bot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(
            users = True, everyone = False, roles = False, replied_user = True
        )
        super().__init__(
            command_prefix = "t!",
            intents = discord.Intents.all(),
            allowed_mentions = allowed_mentions,
            case_insensitive = True,
            strip_after_prefix = True,
            max_messages = 100,
            owner_ids = [859996173943177226, 685082846993317953, 739443421202087966]
        )

        self.token = os.environ["token"]
        self.lavalink_password = os.environ["lavapass"]
        self.log_webook = os.environ["log_webhook"]
        self.del_snipe = []
        self.last_bump = None

        # Database stuff
        self.MONGO_URI = os.environ["MONGO_URI"]
        self.mongo = AsyncIOMotorClient(self.MONGO_URI)
        self.tags = self.mongo["tags"]["tags"]
        self.afk = self.mongo["afk"]["afk"]
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.setup_hook(), self.loop)

    def load_exts(self):
        self.load_extension("cogs.tags")
        self.load_extension("cogs.log")
        self.load_extension("cogs.afk")
        self.load_extension("cogs.welc")
        self.load_extension("cogs.utils")
        self.load_extension("jishaku")

    async def setup_hook(self):
        self.start_time = discord.utils.utcnow()
        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession()

        self.load_exts()
        self.loop.create_task(
            webserver.app.run_task(
                host = "0.0.0.0",
                use_reloader = False
            ) 
        )


    async def on_ready(self):
        await self.get_cog("Afk").update_cache()
        print(f"{self.user} is ready!")

    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.process_commands(after)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.message.add_reaction("⏳")
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send("That command doesn't exist!")
        else:
            err = "".join(
                    traceback.format_exception(
                    etype = type(error),
                    value = error,
                    tb = error.__traceback__
                )
            )
            await ctx.send(
                f"An error occured!\n```{err}```"
            )

# Jishaku config
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_USE_EMBEDS"] = "1"

# Initialize the botto
bot = Bot()

#  Run our botto
bot.run(bot.token, reconnect = True)
