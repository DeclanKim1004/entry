import os
import json
import discord
from discord.ext import commands

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DISCORD_TOKEN = config["token"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


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
