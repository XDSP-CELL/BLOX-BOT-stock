import os
import telebot
from flask import Flask, request

# Telegram Token aur Chat ID
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1882925079")

# Aapka Discord Webhook URL (Reference ke liye yahan stored hai)
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1541694701747576923/qtLddWj-_npom2LzEzRGRF7jl9qejMUfB-1ECZDOj9_JW7aWUaLUaYXmfnwBPG-N59r6"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def discord_webhook():
    data = request.json
    
    # Discord webhook se aane wale data ko check karna
    if data and ("content" in data or "embeds" in data):
        stock_message = data.get("content", "")
        
        # Agar Discord bot embeds (rich cards) bhej raha hai
        embeds = data.get("embeds", [])
        embed_texts = []
        for embed in embeds:
            title = embed.get("title", "")
            description = embed.get("description", "")
            if title: embed_texts.append(f"**{title}**")
            if description: embed_texts.append(description)
            
        full_stock_content = stock_message + "\n" + "\n".join(embed_texts)
        
        if full_stock_content.strip():
            footer_text = "\n\n──────────────────\n👑 **Owner:** @xdsp18\n🛒 **Buy fruit and gamepasses**"
            final_text = f"🔥 *Blox Fruit Live Stock (Discord Sync):*\n\n{full_stock_content.strip()}{footer_text}"
            
            # Telegram par message bhej dena
            bot.send_message(TELEGRAM_CHAT_ID, final_text, parse_mode='Markdown')
            
        return "Success", 200
        
    return "Invalid data", 400

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "🏴‍☠️ Discord-Telegram Live Stock Bridge Active hai!")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
