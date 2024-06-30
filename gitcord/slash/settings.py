import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands

from gitcord.data.database import get_user_defaults


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
        defaults = get_user_defaults(context.author.id, str(context.author))
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
    async def set_defaults(self, context: ApplicationContext) -> None:
        await context.respond(content="Default settings are not yet implemented!", ephemeral=True)


def setup(client) -> None:
    client.add_cog(Settings(client))
