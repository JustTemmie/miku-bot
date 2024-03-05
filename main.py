import discord
from discord.ext import commands

from datetime import datetime
import json
import logging
import asyncio
import glob

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

logging.warning("warning")
logging.error("error")
logging.critical("critical")

with open ("config.json", "r") as f:
    config = json.load(f)

def get_prefix(bot, message):
    return commands.when_mentioned_or(*config["PREFIXES"])(bot, message)

class Miku(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_time = datetime.now()
    
    async def on_ready(self):
        print(f"Succesfully logged in as {self.user}")
    

miku = Miku(
    shards=config["SHARDS"],
    command_prefix=(get_prefix),
    strip_after_prefix=True,
    case_insensitive=True,
    owner_ids=config["OWNER_IDS"],
    intents=discord.Intents.all(),
)

miku.custom_data = {
    "HOST_OWNERS": config["HOST_OWNERS"]
}

tree = miku.tree
# miku.remove_command("help")

async def main():
    async with miku:
        for filename in glob.iglob("./cogs/**", recursive=True):
            if filename.endswith(".py"):
                filename = filename[2:].replace("/", ".")  # goes from "./cogs/economy.py" to "cogs.economy.py"
                await miku.load_extension(f"{filename[:-3]}")  # removes the ".py" from the end of the filename, to make it into cogs.economy
        
        await miku.start(config["TOKEN"])

asyncio.run(main())