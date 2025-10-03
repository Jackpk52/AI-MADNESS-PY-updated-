import discord

# Shared listening channels set
listening_channels = set()

def setup_listen(tree):
    @tree.command(name="listen", description="Toggle AI listening in this channel")
    async def listen(interaction: discord.Interaction):
        channel_id = interaction.channel.id
        
        if channel_id in listening_channels:
            listening_channels.remove(channel_id)
            await interaction.response.send_message(
                f"🔇 **Stopped listening** in <#{channel_id}>\n"
                "I will only respond when mentioned."
            )
        else:
            listening_channels.add(channel_id)
            await interaction.response.send_message(
                f"🎧 **Now listening** in <#{channel_id}>\n"
                "I will respond to all messages here!\n"
                "⚡ Powered by DeepSeek R1 + Groq"
            )