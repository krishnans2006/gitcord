import discord
from discord import ApplicationContext, SlashCommand, SlashCommandGroup, Option
from discord.ext import commands
from discord.commands import slash_command

from bs4 import BeautifulSoup

import re
import requests

from gitcord.config import REMOTES_DEFAULTS
from gitcord.ui.remotes import RemotesView

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

        values = match.groupdict()
        for k, v in values.items():
            if not v:
                values[k] = REMOTES_DEFAULTS[k]

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
        soup = BeautifulSoup(response.text)

        title = soup.find("meta", property="og:title")
        url = soup.find("meta", property="og:url")

        print(title, url)

        view = RemotesView(link)

        await context.respond(content=f"{title}", view=view)


def setup(client) -> None:
    client.add_cog(Remotes(client))
