import discord
from assets.memory import clear_memory

def setup_forget(tree):
    @tree.command(name="forget", description="Clear AI memory in this channel")
    async def forget(interaction: discord.Interaction):
        clear_memory(str(interaction.channel.id))
        await interaction.response.send_message(
            "🧹 **Memory cleared!**\n"
            "I've forgotten our conversation in this channel.\n"
            "⚡ Powered by DeepSeek R1 + Groq"
        )