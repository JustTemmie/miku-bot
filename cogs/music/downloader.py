from discord.ext import commands, tasks

import os
import subprocess
import threading
import logging
import asyncio

class Downloader(commands.Cog):
    def __init__(self, miku):
        self.miku = miku
        self.change_status_task.start()
    
        
    @tasks.loop(hours=27)
    async def change_status_task(self):
        # download assets from spotify
        logging.info("downloading music from Spotify")
        path = os.path.dirname(os.path.realpath(__name__))
        os.chdir("assets/music")
        for i in self.miku.custom_data["SPOTIFY_PLAYLISTS"]:
            logging.info(f"downloading {i}")
            subprocess.run(["../.././venv/bin/python", "-m", "spotdl", i], stdout=subprocess.DEVNULL)
        os.chdir(path)
        logging.info("finished downloading music from Spotify")
    
async def setup(miku):
    await miku.add_cog(Downloader(miku))
