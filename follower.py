import discord
import asyncio
import re
import discord
from discord.ext import commands
import os


TOKEN = os.getenv("DISCORD_BOT_TOKEN")

GUILD_ID = 1364731129575374918
INSTAGRAM_CHANNEL_ID = 1372163475651956797
X_CHANNEL_ID = 1367625135665975388
X2_CHANNEL_ID = 1372163199687983164
COMBINED_CHANNEL_ID = 1370367951659733052

intents = discord.Intents.default()
intents.guilds = True

class FollowerBot(discord.Client):
    async def setup_hook(self):
        self.bg_task = asyncio.create_task(self.update_loop())

    async def on_ready(self):
        print(f'✅ Logged in as {self.user} (ID: {self.user.id})')
        print(f"Guilds: {[g.name for g in self.guilds]}")

    async def extract_number(self, channel_name):
        match = re.search(r'(\d+(?:[\.,]\d+)?)([KMBkmb]?)', channel_name)
        if not match:
            return 0

        number = match.group(1).replace(',', '.')
        suffix = match.group(2).upper()

        multiplier = {
            '': 1,
            'K': 1_000,
            'M': 1_000_000,
            'B': 1_000_000_000,
        }.get(suffix, 1)

        return int(float(number) * multiplier)

    async def update_combined_channel(self):
        guild = self.get_guild(GUILD_ID)
        if guild is None:
            print("❌ Guild not found.")
            return

        insta_channel = guild.get_channel(INSTAGRAM_CHANNEL_ID)
        x1_channel = guild.get_channel(X_CHANNEL_ID)
        x2_channel = guild.get_channel(X2_CHANNEL_ID)
        combined_channel = guild.get_channel(COMBINED_CHANNEL_ID)

        if not all([insta_channel, x1_channel, x2_channel, combined_channel]):
            print("❌ En eller flere kanaler ikke funnet.")
            return

        insta = await self.extract_number(insta_channel.name)
        x1 = await self.extract_number(x1_channel.name)
        x2 = await self.extract_number(x2_channel.name)
        total = insta + x1 + x2
        new_name = f"🌐 Total Followers: {total}"

        print(f"📊 Instagram: {insta}, X1: {x1}, X2: {x2} => Total: {total}")

        if combined_channel.name != new_name:
            await combined_channel.edit(name=new_name)
            print(f"✅ Oppdatert kanalnavn til: {new_name}")
        else:
            print("ℹ️ Ingen endring. Navn er allerede korrekt.")

    async def update_loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                await self.update_combined_channel()
            except Exception as e:
                print(f"⚠️ Feil under oppdatering: {e}")
            await asyncio.sleep(3600)  # Hver time

# Start bot
client = FollowerBot(intents=intents)
client.run(TOKEN)
