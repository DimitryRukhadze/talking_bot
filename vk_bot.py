import random
import logging

from environs import Env

import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from telegram.ext import Updater

from dialogflow_tools import detect_intent
from logging_mod import LoggerHandler


logger = logging.getLogger('dialog_bot_logger')


def send_message(event, vk_api, project_id):
    session_id = f'vk_{event.user_id}'
    answer = detect_intent(project_id, session_id, event.text)
    if not answer.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':

    env = Env()
    env.read_env()

    vk_token = env('VK_API_KEY')
    gcloud_project_id = env('GOOGLE_CLOUD_PROJECT_ID')
    log_chat_id = env('LOG_CHAT_ID')
    tg_token = env('TELEGA_TOKEN')

    updater = Updater(token=tg_token, use_context=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log_handler = LoggerHandler(bot=updater.bot, chat_id=log_chat_id)
    logger.addHandler(log_handler)

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
           try:
               send_message(event, vk_api, gcloud_project_id)
           except Exception as exception:
               logging.debug(exception)
