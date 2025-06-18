import os
import json
import asyncio
import discord
from discord.ext import commands

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DISCORD_TOKEN = config["token"]

OPENING_MESSAGES = [
    "안녕하세요! 서버에 오신 것을 환영합니다.",
    "이 채널에서는 기본 규칙을 안내해 드릴게요.",
    "잠시 후 다른 채널로 이동하실 수 있습니다!",
]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def delete_channel_later(channel: discord.TextChannel, delay: int = 60):
    await asyncio.sleep(delay)
    await channel.delete()

@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    hash_suffix = hex(member.id)[-4:]
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
    }
    channel = await guild.create_text_channel(
        name=f"welcome-{hash_suffix}", overwrites=overwrites
    )
    for msg in OPENING_MESSAGES:
        await channel.send(msg)
        await asyncio.sleep(5)
    asyncio.create_task(delete_channel_later(channel))

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
