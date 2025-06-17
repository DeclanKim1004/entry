import os
import discord
import asyncio

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

OPENING_MESSAGES = [
    "마을의 낯선 이여, 이곳에 처음 오셨군요. 반갑습니다! 🌟",
    "조금만 기다리시면 저희 마을의 간단한 안내를 드리겠습니다.",
    "저는 이 마을을 지키는 안내자, NPC 알베르트입니다.",
    "아래 안내에 따라 #직업선택 채널로 이동해 주세요."
]

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="마을광장")
    if channel is None:
        return
    for msg in OPENING_MESSAGES:
        await channel.send(msg)
        await asyncio.sleep(5)

if __name__ == "__main__":
    bot.run(TOKEN)
