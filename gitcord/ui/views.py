from discord import ButtonStyle
from discord.ui import Button, View


class RemotesView(View):
    def __init__(self, link: str):
        super().__init__(timeout=None)
        self.add_item(Button(label="Open", style=ButtonStyle.link, url=link))
