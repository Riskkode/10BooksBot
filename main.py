import json

with open('settings.json') as f:
    config = json.load(f)
    TOKEN = config['token']

import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed

guild_ids_to_sync = []
import libgen_api
from libgen_api import LibgenSearch
lgs = LibgenSearch()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
results = []
def truncate_string(input_str, max_length=100):
    if len(input_str) <= max_length:
        return input_str
    else:
        return input_str[:max_length-3] + "..."


def get_book_by_id(book_id):
    return next((result for result in results if str(result['ID']) == book_id), None)


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=truncate_string(result['Title']), value=str(result['ID'])) for result in results
        ]
        super().__init__(placeholder='Select a book', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        try:
            selected_value = self.values[0]  # Use self.values[0] to get the selected value
            selected_book = get_book_by_id(selected_value)
            await interaction.response.send_message(f"You have selected {selected_book['Title']}")
            if selected_book:
                download_links = lgs.resolve_download_links(selected_book)

                embed = Embed(title=f"Download links for: {selected_book['Title']}", color=0x00ff00)
                for key, value in download_links.items():
                    formatted_link = f"[{key}]({value})"
                    embed.add_field(name=key, value=formatted_link, inline=False)

                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("Error: Book not found!")
        except Exception as e:
            print(f"An error occurred: {e}")

class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Select())


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    try:
        synced = await tree.sync()  # guild=discord.Object(id=1050223951655219221)
        print(f"Synced {len(synced)} command(s)!")
    except Exception as e:
        print(e)


@tree.command(name="search", description="Search for a book")  # guild=discord.Object(id=1050223951655219221) insert after book
@app_commands.describe(book_title="Input a title to search.", language="Input a language to search.")
@app_commands.choices(
    extension=[
        discord.app_commands.Choice(name="pdf", value="pdf"),
        discord.app_commands.Choice(name="epub", value="epub"),
        discord.app_commands.Choice(name="mobi", value="mobi"),
        discord.app_commands.Choice(name="zip", value="zip")],

    language=[
        discord.app_commands.Choice(name="English", value="English"),
        discord.app_commands.Choice(name="Spanish", value="Spanish"),
        discord.app_commands.Choice(name="German", value="German"),
        discord.app_commands.Choice(name="Dutch", value="Dutch"),
        discord.app_commands.Choice(name="Vietnamese", value="Vietnamese"),
        discord.app_commands.Choice(name="Portuguese", value="Portuguese"),
        discord.app_commands.Choice(name="Chinese", value="Chinese"),
        discord.app_commands.Choice(name="Japanese", value="Japanese"),
        discord.app_commands.Choice(name="French", value="French"),
        discord.app_commands.Choice(name="Italian", value="Italian"),
        discord.app_commands.Choice(name="Korean", value="Korean")
    ])
async def search(interaction, book_title: str, language: discord.app_commands.Choice[str], extension: discord.app_commands.Choice[str]):
    global results
    title_filters = {"Language": language.value, "Extension": extension.value}
    results = lgs.search_title_filtered(book_title, title_filters, exact_match=False)
    if len(results) == 0:
        await interaction.response.send_message("No results found!")
    else:
        await interaction.response.send_message(f"Found {len(results)} results!", view=SelectView())

client.run(TOKEN)



