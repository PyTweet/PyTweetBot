import discord

class Paginator(discord.ui.View):
    def __init__(self, paginator, author, **kwargs):
        super().__init__(
            timeout = 30
        )
        self.paginator: discord.ext.commands.Paginator = paginator
        self.author = author
        self.pages = len(paginator.pages)
        self.page = 1
        self._embed = discord.Embed(colour = discord.Color.red())
        self.embed: discord.Embed = kwargs.pop("embed", self._embed)

    async def update_message(self, interaction):
        self.page_number.label = self.page
        self.embed.description = self.paginator.pages[self.page - 1]
        await interaction.message.edit(embed = self.embed, view = self)

    #Buttons

    @discord.ui.button(label = "First Page", style = discord.ButtonStyle.secondary)
    async def first_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This is not for you", ephemeral = True)
        if self.page == 1:
            return
        self.page = 1
        await self.update_message(interaction)

    @discord.ui.button(style = discord.ButtonStyle.secondary, emoji = "◀️")
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This is not for you", ephemeral = True)
        page = self.page
        if page == 1:
            self.page = self.pages
        else:
            self.page -= 1
        await self.update_message(interaction)

    @discord.ui.button(label = 1, style = discord.ButtonStyle.primary)
    async def page_number(self, button: discord.ui.Button, interaction: discord.Interaction):
        return

    @discord.ui.button(style = discord.ButtonStyle.secondary, emoji = "▶️")
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This is not for you", ephemeral = True)
        page = self.page
        if page == self.pages:
            self.page = 1
        else:
            self.page += 1
        await self.update_message(interaction)

    @discord.ui.button(label = "Last Page", style = discord.ButtonStyle.secondary)
    async def last_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            return await interaction.response.send_message("This is not for you", ephemeral = True)
        if self.page == self.pages:
            return
        self.page = self.pages
        await self.update_message(interaction)