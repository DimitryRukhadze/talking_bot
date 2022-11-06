from environs import Env

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import storage, dialogflow

from dialogue_tools import detect_intent


env = Env()
env.read_env()

TG_TOKEN = env('TELEGA_TOKEN')
GCLOUD_PROJECT_ID = env('GOOGLE_CLOUD_PROJECT_ID')


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
        chat_id=update.effective_chat.id,
        text=intent.query_result.fulfillment_text
    )


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


def authenticate_implicit_with_adc(project_id):

    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


if __name__ == '__main__':

    updater = Updater(token=TG_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    message_hadler = MessageHandler(Filters.text & (~Filters.command), answer_intent)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_hadler)

    updater.start_polling()
    updater.idle()
