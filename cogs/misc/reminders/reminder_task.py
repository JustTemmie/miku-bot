from discord.ext import commands, tasks

import time

import hatsune_miku.database as DbLib


class reminderTask(commands.Cog):
    def __init__(self, miku):
        self.miku = miku

        self.reminder_task.start()

    @tasks.loop(seconds=5)
    async def reminder_task(self):
        data = DbLib.reminder_database.read()
        
        for reminder in data:
            if time.time() >= float(reminder[1]):
                userobj = await self.miku.fetch_user(reminder[2])
                await userobj.send(f"**Reminder:** {reminder[3]}")
                
                DbLib.reminder_database.delete(reminder[0])


async def setup(bot):
    await bot.add_cog(reminderTask(bot))
