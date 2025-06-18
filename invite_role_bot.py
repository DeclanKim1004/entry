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

# Mapping from emoji to job role names used for reaction role assignment.
ROLE_EMOJIS = {
    "⚔️": "전사",
    "🧙": "마법사",
    "🥷": "암살자",
}


async def delete_channel_later(
    channel: discord.TextChannel,
    role: discord.Role | None = None,
    delay: int = 300,
) -> None:
    """Delete the given channel (and role) after a delay in seconds."""
    await asyncio.sleep(delay)
    if role is not None:
        # Delete the role if it still exists. Removing the role will also
        # automatically unassign it from any members.
        guild_role = channel.guild.get_role(role.id)
        if guild_role is not None:
            await guild_role.delete(reason="welcome channel cleanup")

    await channel.delete(reason="welcome channel cleanup")


async def ask_for_job(
    channel: discord.TextChannel,
    member: discord.Member,
    private_role: discord.Role,
) -> None:
    """Ask the member to choose a job via reactions and grant the role."""
    description = "\n".join(f"{emoji} : {name}" for emoji, name in ROLE_EMOJIS.items())
    prompt = await channel.send(
        "원하는 직업의 이모지를 눌러 주세요:\n" + description
    )

    for emoji in ROLE_EMOJIS.keys():
        await prompt.add_reaction(emoji)

    def check(reaction: discord.Reaction, user: discord.User) -> bool:
        return (
            reaction.message.id == prompt.id
            and user.id == member.id
            and str(reaction.emoji) in ROLE_EMOJIS
        )

    try:
        reaction, _ = await bot.wait_for("reaction_add", check=check, timeout=60)
    except asyncio.TimeoutError:
        await channel.send("시간이 초과되어 채널을 정리합니다.")
    else:
        role_name = ROLE_EMOJIS[str(reaction.emoji)]
        role = discord.utils.get(channel.guild.roles, name=role_name)
        if role is None:
            role = await channel.guild.create_role(name=role_name)
        await member.add_roles(role)
        await channel.send(f"{member.mention}님께 {role.name} 역할을 부여했어요!")

    asyncio.create_task(delete_channel_later(channel, private_role, delay=60))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


async def create_invite_channel(
    guild: discord.Guild, member: discord.Member
) -> tuple[discord.TextChannel, discord.Role]:
    """Create a private role and channel for the given member."""

    role_name = f"🔒임시역할-{member.id}"
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
        name=f"비공개-{member.id}",
        overwrites=overwrites,
        reason="신규 사용자 전용 채널",
    )
    return channel, role


@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    channel, private_role = await create_invite_channel(guild, member)

    for msg in OPENING_MESSAGES:
        await channel.send(msg)
        await asyncio.sleep(5)

    await ask_for_job(channel, member, private_role)


@bot.command(name="초대")
async def invite_channel(ctx, member: discord.Member):
    guild = ctx.guild
    channel, private_role = await create_invite_channel(guild, member)
    await ctx.send(
        f"\ud83c\udf39 {member.mention}\ub2d8\uc744 \uc704\ud55c \ucc44\ub110 {channel.mention}\uc774 \uc0dd\uc131\ub418\uc5c8\uc5b4\uc694."
    )

    await ask_for_job(channel, member, private_role)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
