import asyncio
import subprocess
import sys
import os

async def main():
    print("🤖 Starting AI Madness Bot...")
    print("⚡ Powered by DeepSeek R1 + Groq")
    print("📡 Deploying commands...")
    
    try:
        # Run deploy commands directly using asyncio
        from deploy_commands import setup_commands
        await setup_commands()
        
        print("✅ Commands deployed successfully!")
        print("🚀 Starting bot...")
        
        # Run main bot
        from main import bot
        await bot.start(os.getenv('DISCORD_TOKEN'))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())