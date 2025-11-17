import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Wczytaj token z .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True

class VerifyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=None  # automatycznie ustawi się przy logowaniu
        )

    async def setup_hook(self):
        # Załaduj cogi (moduły)
        await self.load_extension("verify")
        await self.tree.sync()
        print("✅ Komendy slash zsynchronizowane")

    async def on_ready(self):
        print(f"🤖 Zalogowano jako {self.user} ({self.user.id})")

# Uruchom bota
bot = VerifyBot()
bot.run(TOKEN)
