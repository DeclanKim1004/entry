# Discord RPG Opening Scenario

This repository contains a simple script example for a Discord RPG-style opening.
It guides new users through the introductory channel `#마을광장`, encourages them to greet other villagers there, and then leads them to select a job in `#직업선택`.

## Files
- `invite_role_bot.py`: Discord bot using `discord.py` to create temporary invitation channels.
- `welcome_bot.py`: Demonstrates creating a private welcome channel for new members.

## Usage
1. Install dependencies: `pip install -r requirements.txt`
   - Main packages: `fastapi`, `uvicorn`, `Flask`, `requests`, `PyMySQL`,
     `discord.py`, `nest_asyncio`, `pyngrok`, and `PyJWT`.
2. Create a `config.json` file in the same directory as `invite_role_bot.py` with the following structure (this file is ignored by git):

   ```json
   {
       "token": "YOUR_DISCORD_TOKEN",
       "database": {},
       "guild_id": 0
   }
   ```

3. Run the bot: `python invite_role_bot.py`
4. To test the welcome scenario, run `python welcome_bot.py`

Use the `초대` command to invite a member. The bot grants a temporary role and
creates a private channel they can access. The channel is automatically
generated for short-term conversations and can be removed afterwards.
The cleanup now happens just 10 seconds after the user picks a role or the
selection times out.

This script showcases the conversation flow described in the previous scenario.
