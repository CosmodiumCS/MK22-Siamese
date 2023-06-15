#!/usr/bin/env python3

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def split(ctx, file_name: str):
    file_path = os.path.join(os.getcwd(), file_name)

    if not os.path.isfile(file_path):
        await ctx.send(f"File '{file_name}' not found.")
        return

    guild = ctx.guild
    category = await guild.create_category("Split Files")

    # Create a new channel for split files
    channel_name = f"split-{file_name}"
    channel = await guild.create_text_channel(channel_name, category=category)

    output_directory = os.path.join(os.getcwd(), "split-files")
    os.makedirs(output_directory, exist_ok=True)

    # Split the file into parts
    with open(file_path, "rb") as file:
        chunk_size = 25 * 1024 * 1024  # 25 MB
        part_num = 1
        parts_list = []  # List to store the part names

        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            part_name = f"{file_name}.part{part_num}"
            part_path = os.path.join(output_directory, part_name)

            with open(part_path, "wb") as part_file:
                part_file.write(chunk)

            await channel.send(file=discord.File(part_path))
            parts_list.append(part_name)
            part_num += 1

    # Create the split record file
    record_file_name = f"{file_name}.record"
    record_file_path = os.path.join(output_directory, record_file_name)

    with open(record_file_path, 'w') as record_file:
        record_file.write("\n".join(parts_list))

    # Upload the split record file
    await channel.send(file=discord.File(record_file_path))

    await ctx.send(f"File '{file_name}' split into parts in channel '{channel_name}'. "
                   f"Split record file '{record_file_name}' created and uploaded.")

@bot.command()
async def download(ctx, channel_name: str):
    guild = ctx.guild

    # Find the channel by name
    channel = discord.utils.get(guild.text_channels, name=channel_name)

    if not channel:
        await ctx.send(f"Channel '{channel_name}' not found.")
        return

    directory = "downloads"  # Directory to save the downloaded files
    os.makedirs(directory, exist_ok=True)

    async for message in channel.history(limit=None):
        attachments = message.attachments
        for attachment in attachments:
            await attachment.save(os.path.join(directory, attachment.filename))

    await ctx.send("Files downloaded successfully.")

@bot.command()
async def rebuild(ctx):
    guild = ctx.guild

    # Request the path and name of the record file from the user
    await ctx.send("Please provide the path and name of the record file:")
    try:
        record_file_path = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Record file input timed out. Please try again.")
        return

    # Validate the record file path and name
    record_file_path = record_file_path.content.strip()
    if not os.path.isfile(record_file_path):
        await ctx.send(f"Record file '{record_file_path}' not found.")
        return

    # Get the directory path of the record file
    record_file_dir = os.path.dirname(record_file_path)

    # Rebuild the file
    output_file_name = input("Enter the name for the rebuilt file: ")
    output_file_path = os.path.join(os.getcwd(), output_file_name)

    with open(record_file_path, 'r') as record_file, open(output_file_path, 'wb') as output_file:
        for line in record_file:
            part_name = line.strip()
            part_path = os.path.join(record_file_dir, part_name)

            if not os.path.isfile(part_path):
                await ctx.send(f"Part file '{part_name}' not found. Rebuild aborted.")
                return

            with open(part_path, 'rb') as part_file:
                output_file.write(part_file.read())

    await ctx.send(f"File '{output_file_name}' successfully rebuilt from split files.")

@bot.command()
async def list(ctx):
    """
    List all available commands and their descriptions.
    
    Syntax: !list
    Example: !list
    
    This command lists all the available commands in the bot along with their syntax and a brief description of how they work.
    """
    command_list = [
        "!split <file_name>",
        "!download <channel_name>",
        "!rebuild",
        "!list"
    ]

    description_list = [
        "Split a file into parts and send them as messages in a text channel.",
        "Download all attachments from a specified channel to the 'downloads' directory.",
        "Rebuild a file from split parts using a record file.",
        "List all available commands and their descriptions."
    ]

    embed = discord.Embed(title="Bot Commands")
    for i in range(len(command_list)):
        embed.add_field(name=command_list[i], value=description_list[i], inline=False)

    await ctx.send(embed=embed)
TOKEN = os.getenv(TOKEN)
bot.run(TOKEN)

# Uhhh im bad at comments ig, made by HL0#8086 on discord, also known as Hall0wed, any problems with the program or questions ask me lol, enjoy splitting files hahahahahhahahahahahahahahahahha
