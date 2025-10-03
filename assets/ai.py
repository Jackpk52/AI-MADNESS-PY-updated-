import os
import groq
import random
import asyncio

# Initialize the Groq client
client = None

async def generate_ai_response(prompt, session=None):
    global client
    
    # Initialize client if not already done
    if client is None:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return "❌ Groq API key not configured. Please set GROQ_API_KEY in .env file."
        client = groq.AsyncGroq(api_key=api_key)
    
    clean_prompt = prompt.replace('<@!?\\d+>', '').strip()
    
    if not clean_prompt:
        return "Hello! How can I help you today?"

    try:
        # Use DeepSeek model through Groq
        chat_completion = await asyncio.wait_for(
            client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[
                    {
                        "role": "user",
                        "content": clean_prompt,
                    },
                ],
                temperature=0.6,
                max_tokens=1024,  # Reduced for Discord limits
                top_p=0.95,
                stream=False,
                stop=None
            ),
            timeout=15.0
        )

        ai_response = chat_completion.choices[0].message.content
        
        if ai_response:
            return ai_response
        else:
            return generate_fallback_response(clean_prompt)

    except asyncio.TimeoutError:
        print("🤖 Groq API Timeout - using fallback")
        return generate_fallback_response(clean_prompt)
    except Exception as error:
        print(f"🤖 Groq API Error: {error}")
        return generate_fallback_response(clean_prompt)

# Smart fallback responses
def generate_fallback_response(prompt):
    lower_prompt = prompt.lower()
    
    if any(word in lower_prompt for word in ['hello', 'hi', 'hey']):
        return "👋 Hello! I'm AI Madness Bot powered by DeepSeek via Groq! How can I help you today?"
    elif 'how are you' in lower_prompt:
        return "I'm doing great! Running on DeepSeek R1 via Groq's lightning-fast API! 🚀"
    elif 'thank' in lower_prompt:
        return "You're welcome! 😊"
    elif '?' in lower_prompt:
        return "That's a great question! How can I assist you further?"
    elif any(word in lower_prompt for word in ['bot', 'madness']):
        return "🤖 That's me! AI Madness Bot - powered by DeepSeek R1 through Groq!"
    elif any(word in lower_prompt for word in ['groq', 'deepseek', 'r1']):
        return "⚡ Yes! I'm using DeepSeek R1 via Groq API - the best of both worlds: powerful reasoning with lightning speed!"
    
    responses = [
        "That's interesting! Tell me more!",
        "I see what you mean! What would you like to discuss?",
        "Fascinating! I'd love to hear more about that.",
        "I understand. How can I help you further?",
        "That's a great point! What else is on your mind?"
    ]
    
    return random.choice(responses)