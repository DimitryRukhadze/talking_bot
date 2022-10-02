from environs import Env

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I work!'
    )

def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )

env = Env()
env.read_env()

tg_token = env('TELEGA_TOKEN')
updater = Updater(token=tg_token, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
message_hadler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_hadler)

updater.start_polling()
updater.idle()
