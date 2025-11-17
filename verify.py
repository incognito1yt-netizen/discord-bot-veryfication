import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setverifychannel", description="Ustaw kanał i rolę do weryfikacji.")
    @app_commands.describe(kanał="Kanał z wiadomością weryfikacyjną", rola="Rola do nadania po weryfikacji")
    async def setverifychannel(self, interaction: discord.Interaction, kanał: discord.TextChannel, rola: discord.Role):
        embed = discord.Embed(
            title="✅ Weryfikacja",
            description="Kliknij reakcję ✅, aby się zweryfikować i uzyskać dostęp do serwera.",
            color=discord.Color.green()
        )

        message = await kanał.send(embed=embed)
        await message.add_reaction("✅")

        data = {
            "guild_id": interaction.guild.id,
            "channel_id": kanał.id,
            "message_id": message.id,
            "role_id": rola.id
        }

        with open("verify.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message(
            f"✅ Kanał ustawiony na {kanał.mention}, rola: {rola.mention}",
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # Ignoruj boty
        if payload.member is None or payload.member.bot:
            return

        # Sprawdź, czy plik istnieje
        if not os.path.exists("verify.json"):
            return

        with open("verify.json") as f:
            data = json.load(f)

        # Sprawdź reakcję i wiadomość
        if (
            payload.message_id == data["message_id"]
            and str(payload.emoji) == "✅"
        ):
            guild = self.bot.get_guild(data["guild_id"])
            role = guild.get_role(data["role_id"])
            member = guild.get_member(payload.user_id)

            if role not in member.roles:
                await member.add_roles(role)
                try:
                    await member.send(f"✅ Zostałeś zweryfikowany na serwerze **{guild.name}**!")
                except discord.Forbidden:
                    pass

async def setup(bot):
    await bot.add_cog(Verify(bot))
