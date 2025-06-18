import os
import json
import asyncio
import discord
from discord.ext import commands

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DISCORD_TOKEN = config["token"]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Messages sent to new members when they join the server. Adjust the content as
# needed for your community.
OPENING_MESSAGES = [
    "어서 오세요! 먼저 #마을광장 채널에서 주민들에게 인사해 보세요.",
    "인사를 마쳤다면, #직업선택 채널에서 원하는 직업을 골라 보세요.",
    "즐거운 시간 되세요!"
]


async def delete_channel_later(channel: discord.TextChannel, delay: int = 300):
    """Delete the given channel after a delay in seconds."""
    await asyncio.sleep(delay)
    await channel.delete(reason="welcome channel cleanup")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    hash_suffix = hex(member.id)[-4:]
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        guild.me: discord.PermissionOverwrite(
            read_messages=True, send_messages=True
        ),
    }

    channel = await guild.create_text_channel(
        name=f"welcome-{hash_suffix}",
        overwrites=overwrites,
    )

    for msg in OPENING_MESSAGES:
        await channel.send(msg)
        await asyncio.sleep(5)

    asyncio.create_task(delete_channel_later(channel))


@bot.command(name="초대")
async def invite_channel(ctx, member: discord.Member):
    guild = ctx.guild
    role_name = f"🔒임시초대-{member.id}"
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        role = await guild.create_role(name=role_name)
        await ctx.send(f"✅ 역할 `{role_name}` 생성 완료")

    await member.add_roles(role)
    await ctx.send(f"🎟️ {member.mention}님에게 `{role_name}` 역할을 부여했어요.")

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        ctx.author: discord.PermissionOverwrite(view_channel=True),
    }

    channel = await guild.create_text_channel(
        name=f"비공개-{member.id}",
        overwrites=overwrites,
        reason="임시 비공개 대화방 생성",
    )
    await channel.send(f"🌟 {member.mention}님, 이곳은 당신만을 위한 방입니다!")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
