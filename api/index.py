from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = "7927385130:AAFuYQJNfFTW1OJpGezQKIl2R1Q4ZKLj9xw"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# Admins
ADMINS = [6411315434]

def start(update, context):
    update.message.reply_text("Bot is online.")

def welcome(update, context):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"Welcome, {member.full_name}!")

def rules(update, context):
    update.message.reply_text("Group Rules:\n1. No spam\n2. No links\n3. Be respectful")

def ban(update, context):
    if update.effective_user.id not in ADMINS:
        update.message.reply_text("Not allowed.")
        return
    if context.args:
        user_id = int(context.args[0])
        bot.kick_chat_member(update.message.chat_id, user_id)
        update.message.reply_text(f"Banned {user_id}.")

def anti_link(update, context):
    if any(x in update.message.text for x in ['http', 't.me', '@']):
        if update.effective_user.id not in ADMINS:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

@app.route("/", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, workers=0, use_context=True)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, anti_link))
    dp.process_update(update)
    return "OK", 200
