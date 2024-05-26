import discord
from discord import ApplicationContext, SlashCommand, SlashCommandGroup
from discord.ext import commands
from discord.commands import slash_command


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.cogs = [cog for cog in self.client.cogs.keys()]
        self.text = ""

    @slash_command(
        name="help",
        description="Show this help message",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def help(self, context: ApplicationContext) -> None:
        await context.defer(ephemeral=True)
        text = ""
        if not self.text:
            self.cogs = [c for c in self.client.cogs.keys()]
            for cog in self.cogs:
                cog = self.client.get_cog(cog)
                text += f"\n\n**All `{cog.qualified_name}` Commands:**\n"
                for cmd in cog.get_commands():
                    if isinstance(cmd, SlashCommand):
                        text += f" • {cmd.mention} - {cmd.description}\n"
                    if isinstance(cmd, SlashCommandGroup):
                        for subcmd in cmd.walk_commands():
                            if isinstance(subcmd, SlashCommand):
                                text += f" • {subcmd.mention} - {subcmd.description}\n"
            self.text = text.lstrip()
        await context.respond(
            content=self.text,
            ephemeral=True,
        )


def setup(client) -> None:
    client.add_cog(Help(client))
