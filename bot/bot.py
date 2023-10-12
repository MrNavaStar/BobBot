import discord
from discord.ext import commands
from discord import Activity
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from requests import get
import nbtreader
from stream import ResponseStream
import io
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def theme(ctx):
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()

        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.play(discord.FFmpegPCMAudio("bot/theme.mp3"))
        while voice_channel.is_playing():
            await asyncio.sleep(.1)
        await voice_channel.disconnect()


@bot.event
async def on_ready():
    print(f"Successfully logged in as: {bot.user}")
    await bot.change_presence(activity=None)


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if len(message.attachments) == 0 or message.author == bot.user:
        return

    bom, items = createBOM(message.attachments)
    if bom is None or items is None:
        return

    await message.channel.send("### BLOCKS:", file=bom, reference=message)
    await message.channel.send("### ITEMS:", file=items, reference=message)


def createBOM(attachments):
    for attachment in attachments:
        if ".nbt" in attachment.url or ".schem" in attachment.url:
            data = get(attachment.url, stream=True)

            blockList, itemList = "", ""
            if ".nbt" in attachment.url:
                blockList, itemList = nbtreader.createBOMFile(ResponseStream(data.iter_content(64)))
            if ".schem" in attachment.url:
                blockList, itemList = nbtreader.createBOMFileSchema(ResponseStream(data.iter_content(64)))

            if blockList == "":
                blockList = "No Blocks Found In Structure"

            if itemList == "":
                itemList = "No Items Found In Structure"

            return discord.File(filename="BOM.txt", fp=io.BytesIO(bytes(blockList, 'utf-8'))), discord.File(filename="Items.txt", fp=io.BytesIO(bytes(itemList, 'utf-8')))
    return None, None


if __name__ == '__main__':
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    bot.run(env.get("DISCORD_BOT_TOKEN"))
