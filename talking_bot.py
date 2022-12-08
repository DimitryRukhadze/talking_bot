import logging

from environs import Env

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialogflow_tools import detect_intent
from logging_mod import LoggerHandler


logger = logging.getLogger('dialog_bot_logger')


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I work!'
    )


def answer_intent(update, context, project_id=''):
    texts = update.message.text
    chat_id = update.effective_chat.id
    intent = detect_intent(project_id, chat_id, text=texts)
    context.bot.send_message(
        chat_id=chat_id,
        text=intent.query_result.fulfillment_text
    )


def main():
    env = Env()
    env.read_env()

    tg_token = env('TELEGA_TOKEN')
    log_chat_id = env('LOG_CHAT_ID')
    gcloud_project_id = env('GOOGLE_CLOUD_PROJECT_ID')

    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log_handler = LoggerHandler(bot=updater.bot, chat_id=log_chat_id)
    logger.addHandler(log_handler)

    start_handler = CommandHandler('start', start)
    message_hadler = MessageHandler(Filters.text & (~Filters.command), lambda answer_intent: answer_intent(project_id=gcloud_project_id))

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_hadler)

    updater.start_polling()
    logger.info('Диалоговый бот запущен!')
    updater.idle()


if __name__ == '__main__':
    main()

