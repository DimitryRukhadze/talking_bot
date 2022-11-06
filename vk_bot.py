import random

from environs import Env

import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType

from dialogue_tools import detect_intent


def send_message(event, vk_api, project_id):
    chat_id = f'vk_{event.user_id}'
    answer = detect_intent(project_id, chat_id, event.text)
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

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
           send_message(event, vk_api, gcloud_project_id)
