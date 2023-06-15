#!/usr/bin/env python3

import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
import re
import asyncio

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

database_file = "database.json"

created_parts = []  # Define the created_parts list outside of the split command


def entry_exists(json_entry):
    if not os.path.isfile(database_file):
        return False

    with open(database_file, "r") as database:
        for line in database:
            try:
                entry = json.loads(line.strip())
                if entry == json_entry:
                    return True
            except json.JSONDecodeError:
                continue
    return False


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
    guild_data = {
        "guild_id": str(guild.id),
        "guild_name": guild.name
    }
    category = await get_or_create_category(guild, "split_files")

    # Create a new channel for split files
    channel_name = f"split-{sanitize_channel_name(get_filename(file_name))}"
    channel = await get_or_create_channel(guild, channel_name, category)

    output_directory = os.path.join(os.getcwd(), "split_files")
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

            part_name = f"{get_filename(file_name)}.part{part_num}"
            part_path = os.path.join(output_directory, part_name)

            with open(part_path, "wb") as part_file:
                part_file.write(chunk)

            await channel.send(file=discord.File(part_path))
            parts_list.append(part_name)
            created_parts.append(part_path)  # Add the part path to the created_parts list
            part_num += 1

    # Create the JSON entry
    json_entry = {
        "file_name": get_filename(file_name),
        "channel_name": channel_name,
        "parts_list": parts_list,
        "guild_data": guild_data
    }

    # Check if the entry already exists in the database
    if not entry_exists(json_entry):
        # Write the JSON entry to the database
        with open(database_file, "a") as database:
            database.write(json.dumps(json_entry) + "\n")

    # Upload the JSON entry to the channel
    json_str = json.dumps(json_entry, indent=4)
    await ctx.send(f"```json\n{json_str}\n```")
    await ctx.send(f"File '{file_name}' split into parts in channel '{channel_name}'. "
                   f"JSON entry created and uploaded.")

    # Delete the created parts
    for part_path in created_parts:
        os.remove(part_path)
    created_parts.clear()


@bot.command()
async def rebuild(ctx):
    guild = ctx.guild

    # Read the JSON entries from the database
    entries = []
    with open(database_file, "r") as database:
        for line in database:
            try:
                entry = json.loads(line.strip())
                entries.append(entry)
            except json.JSONDecodeError:
                continue

    # Display the entries to the user
    if not entries:
        await ctx.send("No split files found.")
        return

    for index, entry in enumerate(entries, start=1):
        channel_name = entry["channel_name"]
        guild_id = entry["guild_data"]["guild_id"]
        guild_name = entry["guild_data"]["guild_name"]
        await ctx.send(f"{index}. File: {entry['file_name']}, Channel: {channel_name}, Guild ID: {guild_id}, Guild Name: {guild_name}")

    await ctx.send("Select the number of the entry to rebuild:")

    # Wait for user input
    try:
        message = await bot.wait_for("message", check=lambda m: m.author == ctx.author, timeout=30)
        selection = int(message.content.strip())
    except (asyncio.TimeoutError, ValueError):
        await ctx.send("Invalid selection or timeout.")
        return

    if selection < 1 or selection > len(entries):
        await ctx.send("Invalid selection.")
        return

    selected_entry = entries[selection - 1]
    channel_name = selected_entry["channel_name"]
    guild_id = int(selected_entry["guild_data"]["guild_id"])
    guild_name = selected_entry["guild_data"]["guild_name"]

    guild = bot.get_guild(guild_id)
    if not guild:
        await ctx.send(f"Guild '{guild_name}' not found.")
        return

    channel = discord.utils.get(guild.channels, name=channel_name)
    if not channel:
        await ctx.send(f"Channel '{channel_name}' not found.")
        return

    output_directory = os.path.join(os.getcwd(), "rebuild_files")
    os.makedirs(output_directory, exist_ok=True)

    # Download the split files from the channel
    for part_name in selected_entry["parts_list"]:
        part_path = os.path.join(output_directory, part_name)

        async for message in channel.history(limit=None):
            if message.attachments:
                attachment = message.attachments[0]
                if attachment.filename == part_name:
                    await attachment.save(part_path)
                    break

    await ctx.send(f"Split files downloaded from channel '{channel_name}' in the guild '{guild.name}'.")

    # Rebuild the file
    file_name = selected_entry["file_name"]
    rebuilt_file_path = os.path.join(output_directory, file_name)

    with open(rebuilt_file_path, "wb") as rebuilt_file:
        for part_name in selected_entry["parts_list"]:
            part_path = os.path.join(output_directory, part_name)
            with open(part_path, "rb") as part_file:
                rebuilt_file.write(part_file.read())

    await ctx.send(f"File '{file_name}' rebuilt. Final file created.")

    # Cleanup - Delete downloaded parts
    for part_name in selected_entry["parts_list"]:
        part_path = os.path.join(output_directory, part_name)
        os.remove(part_path)

    # Cleanup - Delete channel and uploaded JSON file
    json_file_path = os.path.join(output_directory, f"{get_filename(file_name)}.json")
    os.remove(json_file_path)

@bot.command()
async def list(ctx):
    embed = discord.Embed(title="Command List", description="List of available commands:", color=discord.Color.blue())

    embed.add_field(name="!split <file_name>", value="Splits a file into parts and sends them as attachments in the created channel.")
    embed.add_field(name="!rebuild", value="Rebuilds a file from split parts using the `database.json`.")
    embed.add_field(name="!list", value="Lists all the commands and their descriptions.")

    await ctx.send(embed=embed)

async def get_or_create_category(guild, name):
    category = discord.utils.get(guild.categories, name=name)
    if not category:
        category = await guild.create_category(name)
    return category


async def get_or_create_channel(guild, name, category):
    channel_name = sanitize_channel_name(name)
    channel = discord.utils.get(guild.channels, name=channel_name, category=category)
    if not channel:
        channel = await category.create_text_channel(channel_name)
    return channel

def get_filename(file_path):
    return os.path.basename(file_path)

def sanitize_channel_name(name):
    sanitized_name = re.sub(r"[/\\.:]+", "", name)
    return sanitized_name

# Create the database file if it doesn't exist
if not os.path.isfile(database_file):
    with open(database_file, "w") as database:
        pass

bot.run(os.getenv("TOKEN"))