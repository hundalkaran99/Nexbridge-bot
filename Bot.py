import os
import anthropic
import telebot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

conversation_history = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi! I'm Nexbridge 🏠 Your personal AI assistant. Ask me anything!")

@bot.message_handler(commands=['new'])
def new_chat(message):
    conversation_history[message.chat.id] = []
    bot.reply_to(message, "Starting a new conversation! What's on your mind?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_text = message.text

    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    conversation_history[chat_id].append({
        "role": "user",
        "content": user_text
    })

    bot.send_chat_action(chat_id, 'typing')

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system="You are Nexbridge, a helpful personal AI assistant. Answer any question clearly and helpfully.",
        messages=conversation_history[chat_id]
    )

    answer = response.content[0].text

    conversation_history[chat_id].append({
        "role": "assistant",
        "content": answer
    })

    bot.reply_to(message, answer)

bot.polling()
