import os
import json
import discord
import asyncio
from discord.ext import commands

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DISCORD_TOKEN = config["token"]
DB_CONFIG = config.get("database")
GUILD_ID = config.get("guild_id")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

NEWCOMER_ROLE_NAME = "신입"
JOB_ROLES = ["전사", "마법사", "암살자"]
bot = commands.Bot(command_prefix="!", intents=intents)

OPENING_MESSAGES = [
    "마을의 낯선 이여, 이곳에 처음 오셨군요. 반갑습니다! 🌟",
    "조금만 기다리시면 저희 마을의 간단한 안내를 드리겠습니다.",
    "저는 이 마을을 지키는 안내자, NPC 이름모를불꽃입니다.",
    "아래 안내에 따라 #직업선택 채널로 이동해 주세요."
]


async def delete_channel_later(channel: discord.TextChannel, delay: int = 60):
    await asyncio.sleep(delay)
    await channel.delete()


@bot.event
async def on_member_join(member):
    guild = member.guild
    newbie_role = discord.utils.get(guild.roles, name=NEWCOMER_ROLE_NAME)
    if newbie_role is None:
        newbie_role = await guild.create_role(name=NEWCOMER_ROLE_NAME)
    await member.add_roles(newbie_role)
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
    if job not in JOB_ROLES:
        await ctx.send("존재하지 않는 직업입니다.")
        return
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=job)
    if role is None:
        role = await guild.create_role(name=job)
    await ctx.author.add_roles(role)
    newbie_role = discord.utils.get(guild.roles, name=NEWCOMER_ROLE_NAME)
    if newbie_role and newbie_role in ctx.author.roles:
        await ctx.author.remove_roles(newbie_role)
    await ctx.send(f"{ctx.author.mention}님, {job} 직업이 선택되었습니다!")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
