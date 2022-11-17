import logging
from google.cloud import dialogflow

class LoggerHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.shat_id = chat_id

    def emit(self, record):
        entry = self.format(record)
        self.bot.send_message(self.chat_id, text=entry)


def detect_intent(project_id, session_id, text, language_code='ru'):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response