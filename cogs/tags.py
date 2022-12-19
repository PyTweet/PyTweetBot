import discord
from discord.ext import commands

import views


class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.tags

    @commands.group(name="tag", invoke_without_command=True)
    async def _tag(self, ctx, name: str = None, raw=None):
        """View a tag's content."""
        if name is None:
            return await ctx.send(
                f"__**View a tag**__\n***```{ctx.prefix}tag <name>```***\n__**Create Tag**__\n***```{ctx.prefix}tag create <name> <content>```***\n__**Delete Tag**__\n***```{ctx.prefix}tag delete <name> <content>```***"
            )
        t = await self.tags.find_one({"name": name})
        if t is None:
            return await ctx.send("A tag with this name doesn't exist.")
        if raw:
            return await ctx.send(discord.utils.escape_markdown(t["content"]))
        await ctx.send(t["content"])

    @_tag.group(name="create", aliases=["c"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx, name: str, *, content: str):
        if name is None:
            return await ctx.send(f"Tag name can't be none!")
        for cmd in self.bot.commands:
            if name == cmd.name:
                return await ctx.send(
                    f"You can't create a tag with the same name as a command!"
                )
        t = await self.tags.find_one({"name": name})
        if t is not None:
            return await ctx.send("There is already a tag with this name!")
        if not content:
            return await ctx.respond("Content can't be none!")
        t = {
            "name": name,
            "content": content,
            "owner": ctx.author.id,
            "created": discord.utils.utcnow(),
        }
        await self.tags.insert_one(t)
        await ctx.send(f"Tag **{name}** has been created!")

    @_tag.command(name="edit", aliases=["e"])
    async def edit(self, ctx, name: str, *, content: str):
        t = await self.tags.find_one({"name": name})
        if t is None:
            return await ctx.send(f"Tag called {name} was not found!")
        if ctx.author.id != t.get("owner"):
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("You do not have permission to edit this tag!")

        t["content"] = content
        await self.tags.update_one({"name": name}, {"$set": t})
        await ctx.send(f"Edited {name}!")

    @_tag.command(name="delete", aliases=["d"])
    async def delete(self, ctx, name: str):
        t = await self.tags.find_one({"name": name})
        if t is None:
            return await ctx.send(f"Tag called **{name}** was not found!")
        owner = t["owner"]
        if ctx.author.id != owner:
            if not ctx.author.guild_permissions.administrator:
                return await ctx.send("You do not have permission to delete this tag!")

        await self.tags.delete_one(t)
        await ctx.send(f"Deleted **{name}** tag!")

    @_tag.command(name="list")
    async def _list(self, ctx):
        pag = commands.Paginator(prefix="", suffix="", max_size=500)
        tags = self.tags.find({})

        async for tag in tags:
            pag.add_line(
                f"""
                Name: **{tag.get("name")}**
                Owner: <@{tag.get("owner")}>
                Created: {discord.utils.format_dt(tag.get("created"), "R")}
                """
            )
        try:
            embed = discord.Embed(
                title="Tags", description=pag.pages[0], colour=discord.Colour.blurple()
            )
        except:
            return await ctx.send("There are no tags!")
        pag_view = views.Paginator(pag, ctx, embed=embed)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
        )
        await ctx.send(embed=embed, view=pag_view)


def setup(bot):
    bot.add_cog(Tags(bot))
