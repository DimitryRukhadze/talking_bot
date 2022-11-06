from environs import Env

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import storage, dialogflow


env = Env()
env.read_env()

TG_TOKEN = env('TELEGA_TOKEN')
GCLOUD_PROJECT_ID = env('GOOGLE_CLOUD_PROJECT_ID')


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I work!'
    )


def detect_intent_texts(project_id, session_id, text, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


def answer_intent(update, context):
    language_code = 'ru'
    texts = update.message.text
    chat_id = update.effective_chat.id
    intent = detect_intent_texts(GCLOUD_PROJECT_ID, chat_id, text=texts, language_code=language_code)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=intent
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
