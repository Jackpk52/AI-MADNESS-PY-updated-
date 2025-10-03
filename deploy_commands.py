import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def setup_commands():
    """Setup and sync commands with Discord"""
    if not os.getenv('DISCORD_TOKEN'):
        print("❌ Missing DISCORD_TOKEN in .env")
        return
    if not os.getenv('CLIENT_ID'):
        print("❌ Missing CLIENT_ID in .env")
        return

    # Create a bot instance just for command deployment
    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)
    tree = app_commands.CommandTree(bot)

    # Import and register commands
    from commands.ping import setup_ping
    from commands.details import setup_details
    from commands.listen import setup_listen
    from commands.forget import setup_forget

    @bot.event
    async def on_ready():
        print(f"✅ Logged in as {bot.user}")
        print("🚀 Deploying slash commands...")
        print("⚡ Powered by DeepSeek R1 + Groq")
        
        # Register commands
        setup_ping(tree)
        setup_details(tree)
        setup_listen(tree)
        setup_forget(tree)
        
        try:
            # Sync commands globally
            synced = await tree.sync()
            print(f"✅ Successfully deployed {len(synced)} commands!")
            print(f"📋 Commands: {', '.join([cmd.name for cmd in synced])}")
        except Exception as error:
            print("❌ Error deploying commands:")
            print(error)
        finally:
            await bot.close()

    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(setup_commands())