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

    existing_parts = set()
    for existing_file in os.listdir(output_directory):
        if existing_file.startswith(file_name + ".part"):
            existing_parts.add(existing_file)

    # Split the file into parts
    with open(file_path, "rb") as file:
        chunk_size = 25 * 1024 * 1024  # 25 MB
        part_num = 1


        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            part_name = f"{file_name}.part{part_num}"
            part_path = os.path.join(output_directory, part_name)

            if part_name not in existing_parts:  # Check if the part already exists
                with open(part_path, "wb") as part_file:
                    part_file.write(chunk)

                await channel.send(file=discord.File(part_path))
                existing_parts.add(part_name)

            part_num += 1


    # Create the split record file
    record_file_name = f"{file_name}.record"
    record_file_path = os.path.join(output_directory, record_file_name)


    with open(record_file_path, 'w') as record_file:
        record_file.write("\n".join(existing_parts))


    # Upload the split record file
    await channel.send(file=discord.File(record_file_path))


    await ctx.send(f"File '{file_name}' split into parts in channel '{channel_name}'. "
                   f"Split record file '{record_file_name}' created and uploaded.")



TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)