import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import aiohttp

# Load environment variables
load_dotenv()

# Check environment variables
if not os.getenv('DISCORD_TOKEN'):
    print("❌ Missing DISCORD_TOKEN in .env")
    exit(1)
if not os.getenv('CLIENT_ID'):
    print("❌ Missing CLIENT_ID in .env")
    exit(1)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Global session for AI requests
ai_session = None

# Import command setups
from commands.ping import setup_ping
from commands.details import setup_details
from commands.listen import setup_listen, listening_channels
from commands.forget import setup_forget

# Import assets
from assets.memory import add_to_memory, get_memory
from assets.ai import generate_ai_response

# Rotating status task
async def rotate_status():
    await bot.wait_until_ready()
    
    statuses = [
        discord.Activity(type=discord.ActivityType.watching, name="DeepSeek R1 AI"),
        discord.Activity(type=discord.ActivityType.playing, name="with Advanced Reasoning ⚡")
    ]
    
    while not bot.is_closed():
        for status in statuses:
            await bot.change_presence(activity=status, status=discord.Status.online)
            await asyncio.sleep(10)

# Events
@bot.event
async def on_ready():
    global ai_session
    
    print(f'✅ Logged in as {bot.user.name}')
    print(f'📊 Serving {len(bot.guilds)} servers')
    print('⚡ Powered by DeepSeek R1 + Groq')
    
    # Create global aiohttp session
    ai_session = aiohttp.ClientSession()
    
    # Setup commands
    setup_ping(bot.tree)
    setup_details(bot.tree)
    setup_listen(bot.tree)
    setup_forget(bot.tree)
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Loaded {len(synced)} commands")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")
    
    # Start rotating status
    bot.loop.create_task(rotate_status())
    print("🔄 Rotating status started!")

@bot.event
async def on_disconnect():
    print("🔌 Bot disconnected")

@bot.event
async def on_close():
    global ai_session
    print("🔴 Bot shutting down...")
    
    # Close aiohttp session properly
    if ai_session and not ai_session.closed:
        await ai_session.close()
        print("✅ AI session closed properly")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"Command error: {error}")
    await ctx.send("⚠️ There was an error executing this command.")

# Message handler for AI responses
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # Check if bot is mentioned OR channel is in listening mode
    is_mentioned = bot.user.mentioned_in(message)
    is_listening = message.channel.id in listening_channels
    
    if not is_mentioned and not is_listening:
        return
    
    input_text = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
    
    # If not mentioned and no input, ignore (for listening mode)
    if not is_mentioned and not input_text:
        return
    
    try:
        # Get conversation history
        memory = get_memory(str(message.channel.id))
        
        # Create context from memory
        context = ""
        if memory:
            context = '\n'.join([f"{msg['role']}: {msg['text']}" for msg in memory]) + '\n'
        
        full_prompt = f"{context}user: {input_text}"
        
        # Show typing indicator
        async with message.channel.typing():
            reply = await generate_ai_response(full_prompt, ai_session)
        
        # Add to memory
        add_to_memory(str(message.channel.id), "user", input_text)
        add_to_memory(str(message.channel.id), "assistant", reply)
        
        await message.reply(reply)
    except Exception as err:
        print(f"AI Error: {err}")
        await message.reply("⚠️ AI failed to respond. Please try again.")

# Clean shutdown
async def shutdown():
    global ai_session
    print("🛑 Shutting down bot...")
    
    # Close aiohttp session
    if ai_session and not ai_session.closed:
        await ai_session.close()
        print("✅ AI session closed")
    
    await bot.close()
    print("✅ Bot closed properly")

if __name__ == "__main__":
    try:
        bot.run(os.getenv('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal")
        asyncio.run(shutdown())
    finally:
        print("🎯 Bot process ended")