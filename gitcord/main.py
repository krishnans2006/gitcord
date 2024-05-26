import discord

from gitcord.config import OWNER_ID, DISCORD_TOKEN, TEST_GUILDS, DEBUG

intents = discord.Intents.default()
if DEBUG:
    client = discord.Bot(intents=intents, owner_id=OWNER_ID, test_guilds=TEST_GUILDS)
else:
    client = discord.Bot(intents=intents, owner_id=OWNER_ID)

slash_cogs = ["slash.help", "slash.remotes"]
for cog in slash_cogs:
    client.load_extension(cog)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="with git"))
    print("Ready!")


@client.event
async def on_application_command_error(
    context: discord.ApplicationContext, error: discord.DiscordException
):
    if isinstance(error, discord.ApplicationCommandInvokeError):
        await context.respond(
            f"This command raised an error! Please report this to the developers.\n```py\n{str(error)}\n```",
            ephemeral=True,
        )
    raise error


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN is not set! Please set it in gitcord/config/secret.py")
    client.run(DISCORD_TOKEN)
