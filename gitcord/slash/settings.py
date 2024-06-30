import discord
from discord import ApplicationContext, SlashCommandGroup
from discord.ext import commands


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
        await context.respond(content="Default settings are not yet implemented!", ephemeral=True)

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
