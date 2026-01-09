import discord
from discord.ext import commands
import asyncio
import os
import datetime

# ================= CONFIG =================

VOICE_CHANNEL_ID = 1459023769564741705
FORCED_NAME = "SLAYZ DOXING/CARDING/ASSASSINAT"

# ==========================================

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True


class MyBot(commands.Bot):
    async def setup_hook(self):
        self.loop.create_task(keep_alive())


bot = MyBot(command_prefix="!", intents=intents)

rename_lock = False


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.invisible)
    print(f"✅ Connecté en tant que {bot.user} (statut invisible)")


@bot.event
async def on_guild_channel_update(before, after):
    global rename_lock

    if after.id != VOICE_CHANNEL_ID:
        return

    if not isinstance(after, discord.VoiceChannel):
        return

    if before.name == after.name:
        return

    if rename_lock:
        return

    rename_lock = True
    await asyncio.sleep(2)

    try:
        await after.edit(name=FORCED_NAME)
        print("🔁 Nom du salon rétabli")
    except Exception as e:
        print("❌ Erreur lors du rename :", e)

    await asyncio.sleep(1)
    rename_lock = False


async def keep_alive():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("🟢 Bot actif -", datetime.datetime.now())
        await asyncio.sleep(300)


bot.run(os.environ["TOKEN"])
