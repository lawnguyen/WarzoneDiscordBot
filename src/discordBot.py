import discord

class DiscordBot(discord.Client):

    async def on_ready(self):
        print("Discord bot is ready")
