# Discord RPG Opening Scenario

This repository contains a simple script example for a Discord RPG-style opening.
It guides new users through the introductory channel `#마을광장`, encourages them to greet other villagers there, and then leads them to select a job in `#직업선택`.

## Files
- `bot.py`: Example Discord bot using `discord.py` to demonstrate timed NPC messages for new users.

## Usage
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `config.json` file in the same directory as `bot.py` with the following structure (this file is ignored by git):

   ```json
   {
       "token": "YOUR_DISCORD_TOKEN",
       "database": {},
       "guild_id": 0
   }
   ```

3. Run the bot: `python bot.py`

When a new member joins, the bot assigns them a temporary role called `신입`
and creates a private channel only they can see. After they choose one of the
job roles (`전사`, `마법사`, or `암살자`), the temporary role is removed and the
channel is deleted shortly after the conversation ends. The NPC guiding them is
named **이름모를불꽃**.

This script showcases the conversation flow described in the previous scenario.
