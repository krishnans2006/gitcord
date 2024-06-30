from discord import ButtonStyle
from discord.ui import Button, View


class RemotesView(View):
    def __init__(self, text: str, link: str):
        super().__init__(timeout=None)
        self.add_item(Button(label=text[:75], style=ButtonStyle.gray, disabled=True))
        self.add_item(Button(label="Open", style=ButtonStyle.link, url=link))
