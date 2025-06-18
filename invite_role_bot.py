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


async def create_invite_channel(guild: discord.Guild, member: discord.Member) -> discord.TextChannel:
    """Create a private role and channel for the given member."""
    role_name = f"\ud83d\udd12\uc784\uc2dc\uc695\uc815-{member.id}"
    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        role = await guild.create_role(name=role_name)

    await member.add_roles(role)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }

    channel = await guild.create_text_channel(
        name=f"\ube44\uacf5\uac1c-{member.id}",
        overwrites=overwrites,
        reason="\uc2e0\uad8c \uc0ac\uc6a9\uc790 \uc804\uc6a9 \ucc44\ub110",
    )
    return channel


@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    channel = await create_invite_channel(guild, member)

    for msg in OPENING_MESSAGES:
        await channel.send(msg)
        await asyncio.sleep(5)

    asyncio.create_task(delete_channel_later(channel))


@bot.command(name="초대")
async def invite_channel(ctx, member: discord.Member):
    guild = ctx.guild
    channel = await create_invite_channel(guild, member)
    await ctx.send(
        f"\ud83c\udf39 {member.mention}\ub2d8\uc744 \uc704\ud55c \ucc44\ub110 {channel.mention}\uc774 \uc0dd\uc131\ub418\uc5c8\uc5b4\uc694."
    )


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
