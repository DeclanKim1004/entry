import os
import discord
import asyncio
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

OPENING_MESSAGES = [
    "마을의 낯선 이여, 이곳에 처음 오셨군요. 반갑습니다! 🌟",
    "조금만 기다리시면 저희 마을의 간단한 안내를 드리겠습니다.",
    "저는 이 마을을 지키는 안내자, NPC 알베르트입니다.",
    "아래 안내에 따라 #직업선택 채널로 이동해 주세요."
]


async def delete_channel_later(channel: discord.TextChannel, delay: int = 60):
    await asyncio.sleep(delay)
    await channel.delete()


@bot.event
async def on_member_join(member):
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


@bot.command(name="choose")
async def choose(ctx, *, job: str):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=job)
    if role is None:
        role = await guild.create_role(name=job)
    await ctx.author.add_roles(role)
    await ctx.send(f"{ctx.author.mention}님, {job} 직업이 선택되었습니다!")

if __name__ == "__main__":
    bot.run(TOKEN)
