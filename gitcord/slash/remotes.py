import io

import aiohttp
import discord
from PIL import Image
from discord import ApplicationContext, SlashCommand, SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from bs4 import BeautifulSoup

import re
import requests

from gitcord.config import REMOTES_DEFAULTS as GLOBAL_DEFAULTS
from gitcord.data import database
from gitcord.ui.views import RemotesView

REFERENCE_REGEX = re.compile(
    r"^"
    r"(?!$)"  # Not empty
    r"(?:(?P<remote>gh|gl):+)?"  # gh (GitHub) or gl (GitLab), followed by :
    r"(?:(?P<user>[a-zA-Z0-9-]+)/)?"  # User or organization, followed by /
    r"(?P<repo>[a-zA-Z0-9-]+)?"  # Repository
    r"(?:#(?P<ref>[0-9-]+))?"  # Hashtag, followed by issue or PR number
    r"(?:!(?P<mr>[0-9-]+))?"  # Exclamation mark, followed by MR number
    r"$"
)


class Remotes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @slash_command(
        name="r",
        description="Reference a remote repository",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def reference(
        self,
        context: ApplicationContext,
        ref: Option(str, "Reference string"),
    ) -> None:
        match = REFERENCE_REGEX.match(ref)
        if not match:
            await context.respond(content="Invalid reference string!", ephemeral=True)
            return

        user_defaults = database.get_user_defaults(context.author.id, str(context.author))
        if not user_defaults:
            user_defaults = {}

        values = match.groupdict()
        for k, v in values.items():
            if not v:
                if k in user_defaults:
                    values[k] = user_defaults[k]
                else:
                    values[k] = GLOBAL_DEFAULTS[k]

        remote_key = {"gh": "https://github.com", "gl": "https://gitlab.com"}
        link = f"{remote_key[values['remote']]}/{values['user']}/{values['repo']}"

        if values["remote"] == "gh":
            if values["mr"]:
                await context.respond(
                    content="GitHub does not support MRs (`!...`)", ephemeral=True
                )
                return
            if values["ref"]:
                link += f"/issues/{values['ref']}"
        elif values["remote"] == "gl":
            if values["ref"] and values["mr"]:
                await context.respond(
                    content="Cannot have both a ref (`#...`) and MR (`!...`)", ephemeral=True
                )
                return
            if values["mr"]:
                link += f"/-/merge_requests/{values['mr']}"
            elif values["ref"]:
                link += f"/-/issues/{values['ref']}"
        else:
            await context.respond(content="Invalid remote!", ephemeral=True)
            return

        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("meta", property="og:title").get("content")
        image = soup.find("meta", property="og:image").get("content")
        url = soup.find("meta", property="og:url").get("content")

        print(title, image, url)

        view = RemotesView(link)

        async with aiohttp.ClientSession() as session:
            async with session.get(image) as resp:
                img = await resp.read()
                with io.BytesIO(img) as file:
                    pil = Image.open(file)
                    pil.thumbnail((400, 200), Image.Resampling.LANCZOS)
                    with io.BytesIO() as output_file:
                        pil.save(output_file, format="PNG")
                        output_file.seek(0)
                        discord_file = discord.File(output_file, filename="image.png")

        content = f"{title}" if values["remote"] == "gl" else ""

        await context.respond(content=content, view=view, file=discord_file)


def setup(client) -> None:
    client.add_cog(Remotes(client))
