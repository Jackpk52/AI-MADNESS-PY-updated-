import discord

def setup_details(tree):
    @tree.command(name="details", description="Show basic AI Madness Bot details")
    async def details(interaction: discord.Interaction):
        await interaction.response.send_message(
            "🤖 **AI Madness Bot**\n\n"
            "**Commands:**\n"
            "`/ping` - Check bot latency\n"
            "`/details` - Show this info\n"
            "`/listen` - Toggle AI listening in channel\n"
            "`/forget` - Clear AI memory\n\n"
            "**Features:**\n"
            "• DeepSeek R1 via Groq API ⚡\n"
            "• Advanced reasoning capabilities\n"
            "• Conversation memory (last 10 messages)\n"
            "• Channel listening mode\n"
            "• Slash command support\n\n"
            "**Usage:**\n"
            "Mention me or use `/listen` to activate AI!\n"
            "Powered by DeepSeek R1 + Groq LPU technology!"
        )