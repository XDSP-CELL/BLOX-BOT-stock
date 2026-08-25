import os
import threading
import discord
import telebot
from flask import Flask

# Telegram Credentials
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1882925079")

# Discord Bot Token
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# Telegram Bot Setup
tele_bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
discord_client = discord.Client(intents=intents)

def process_and_send(message):
    # Apne bot ke messages ko ignore karna
    if message.author == discord_client.user:
        return

    text_content = message.content or ""
    embed_contents = []

    # Bloxy Stocks bot ka data jahan bhi chupa ho, use jabardasti nikalna
    if message.embeds:
        for embed in message.embeds:
            data = embed.to_dict()
            if 'author' in data and 'name' in data['author']: embed_contents.append(str(data['author']['name']))
            if 'title' in data: embed_contents.append(str(data['title']))
            if 'description' in data: embed_contents.append(str(data['description']))
            if 'fields' in data:
                for field in data['fields']:
                    embed_contents.append(f"\n{field.get('name', '')}\n{field.get('value', '')}")
            if 'footer' in data and 'text' in data['footer']: embed_contents.append(str(data['footer']['text']))

    full_text = text_content + "\n" + "\n".join(embed_contents)
    full_text = full_text.strip()

    # Agar thoda sa bhi text mila toh bhej do
    if full_text:
        final_message = f"🔥 *Blox Fruit Live Stock:*\n\n{full_text}\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
        try:
            # Markdown ke sath bhejne ki koshish
            tele_bot.send_message(TELEGRAM_CHAT_ID, final_message, parse_mode='Markdown')
        except Exception:
            # Agar emojis ya format ki wajah se error aaye toh simple text bhej do
            tele_bot.send_message(TELEGRAM_CHAT_ID, final_message)

@discord_client.event
async def on_ready():
    print(f"Logged in as {discord_client.user}")
    # Deploy hote hi Telegram par message aayega!
    try:
        tele_bot.send_message(TELEGRAM_CHAT_ID, "✅ **System Online:** Discord to Telegram bridge is now active!")
    except Exception:
        pass

@discord_client.event
async def on_message(message):
    process_and_send(message)

@discord_client.event
async def on_message_edit(before, after):
    process_and_send(after)

# Render ke liye Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

if __name__ == '__main__':
    def run_discord():
        if DISCORD_BOT_TOKEN:
            discord_client.run(DISCORD_BOT_TOKEN)
    
    threading.Thread(target=run_discord).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
