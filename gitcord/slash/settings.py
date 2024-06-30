import discord
from discord import ApplicationContext, SlashCommandGroup, Option
from discord.ext import commands

from gitcord.data import database


class Settings(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    defaults = SlashCommandGroup("defaults", "Configure default settings")

    @defaults.command(
        name="get",
        description="Get default settings",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def get_defaults(self, context: ApplicationContext) -> None:
        defaults = database.get_user_defaults(context.author.id, str(context.author))
        if not defaults:
            await context.respond(
                content=f"You haven't set your defaults yet! Use {self.set_defaults.mention} to do so"
            )
            return
        content = ""
        for key, value in defaults.items():
            content += f"**{key}**: {value}\n"
        await context.respond(content=content, ephemeral=True)

    @defaults.command(
        name="set",
        description="Set default settings",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def set_defaults(
        self,
        context: ApplicationContext,
        remote: Option(
            str,
            description="Default remote server (GitHub or GitLab)",
            choices=("gh", "gl"),
            required=False,
        ),
        user: Option(str, description="Default user or organization", required=False),
        repo: Option(str, description="Default repository", required=False),
    ) -> None:
        choices = {}
        if remote:
            choices["remote"] = remote
        if user:
            choices["user"] = user
        if repo:
            choices["repo"] = repo
        if not choices:
            await context.respond(content="No defaults provided!", ephemeral=True)
            return
        database.set_user_defaults(context.author.id, str(context.author), choices)
        await context.respond(content="Done!", ephemeral=True)


def setup(client) -> None:
    client.add_cog(Settings(client))
