import os
import threading
import discord
import telebot
from flask import Flask

# Telegram Credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1882925079")

# Discord Bot Token (Render Environment Variable se aayega)
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# Telegram Bot Setup
tele_bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f"Logged in as Discord Bot: {discord_client.user}")

@discord_client.event
async def on_message(message):
    # Apne bot ke messages ko ignore karna taaki loop na bane
    if message.author == discord_client.user:
        return

    # Chahe message plain text ho ya kisi bot ka embed/stock card, sabko read karega
    if message.content or message.embeds:
        content = message.content or ""
        embed_texts = []
        
        for embed in message.embeds:
            if embed.title:
                embed_texts.append(f"**{embed.title}**")
            if embed.description:
                embed_texts.append(embed.description)
            # Embed ke andar ke fields (jaise fruits aur unke prices) ko nikalne ke liye
            for field in embed.fields:
                field_name = field.name or ""
                field_value = field.value or ""
                embed_texts.append(f"\n{field_name}\n{field_value}")
                
        full_text = content + "\n" + "\n".join(embed_texts)
        
        # Agar text ya embed mein kuch bhi data hai toh Telegram par bhej dega
        if full_text.strip():
            footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
            final_message = f"🔥 *Blox Fruit Live Stock (Discord Sync):*\n\n{full_text.strip()}{footer_text}"
            
            # Telegram par message bhej dena
            tele_bot.send_message(TELEGRAM_CHAT_ID, final_message, parse_mode='Markdown')

# Render ke liye Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord-Telegram Bridge is Alive!"

if __name__ == '__main__':
    def run_discord():
        if DISCORD_BOT_TOKEN:
            discord_client.run(DISCORD_BOT_TOKEN)
        else:
            print("Error: DISCORD_BOT_TOKEN environment variable is missing!")
        
    t = threading.Thread(target=run_discord)
    t.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
