import discord

def setup_ping(tree):
    @tree.command(name="ping", description="Show Discord API latency")
    async def ping(interaction: discord.Interaction):
        latency = round(interaction.client.latency * 1000)
        await interaction.response.send_message(
            f"🏓 **Pong!**\n"
            f"🌐 API Latency: {latency}ms\n"
            f"⚡ Powered by DeepSeek R1 + Groq"
        )