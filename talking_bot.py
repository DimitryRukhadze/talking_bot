import logging

from environs import Env

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialogue_tools import detect_intent
from logging_mod import LoggerHandler


env = Env()
env.read_env()

TG_TOKEN = env('TELEGA_TOKEN')
GCLOUD_PROJECT_ID = env('GOOGLE_CLOUD_PROJECT_ID')
LOG_CHAT_ID = env('LOG_CHAT_ID')
updater = Updater(token=TG_TOKEN, use_context=True)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I work!'
    )


def answer_intent(update, context):
    texts = update.message.text
    chat_id = update.effective_chat.id
    intent = detect_intent(GCLOUD_PROJECT_ID, chat_id, text=texts)
    context.bot.send_message(
        chat_id=chat_id,
        text=intent.query_result.fulfillment_text
    )


if __name__ == '__main__':

    dispatcher = updater.dispatcher

    logger = logging.getLogger('dialog_bot_logger')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log_handler = LoggerHandler(bot=updater.bot, chat_id=LOG_CHAT_ID)
    logger.addHandler(log_handler)

    start_handler = CommandHandler('start', start)
    message_hadler = MessageHandler(Filters.text & (~Filters.command), answer_intent)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_hadler)

    updater.start_polling()
    logger.info('Диалоговый бот запущен!')
    updater.idle()
