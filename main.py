import os
import telebot
from flask import Flask, request

# Apna Telegram Bot Token yahan dalein
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8921710043:AAGPh-_PdJEiMTSLAwVzEu21f9ZEHFSN3Iw")
# Jis Telegram chat/channel par message bhejna hai uska ID yahan dalein
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def discord_webhook():
    data = request.json
    
    # Discord webhook se aane wala message data check karna
    if data and ("content" in data or "embeds" in data):
        # Agar content me text hai
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
