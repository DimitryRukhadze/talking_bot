Telegram bot и vk bot с использованием Google DialogFlow
===

Эти боты созданы с учебными целями для куров [devman](https://www.dvmn.org). Пример работающего бота напишите ему в Telegram: `@Devman_hobot_bot`, 
или зайдите в группу [Вконтакте](https://vk.com/club212825643).

Начало работы
---

Перед началом работы установите необходимые для работы библиотеки с помощью команды в терминале:
```commandline
pip install -r requirements.txt
```
Затем подключите [Google Cloud](https://cloud.google.com/dialogflow/es/docs/quick/api) и создайте агент в [DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/api).
Также необходимо создать группу [Вконтакте](https://vk.com).

Также необходимо создать `.env` файл, куда нужно поместить необходимые для работы ключи:
```dotenv
TELEGA_TOKEN=Токен Телеграм бота
GOOGLE_CLOUD_PROJECT_ID=Идентификатор проекта в Google Cloud
VK_API_KEY=Ваш ключ к api Вконтакте
```

Запуск и использование
---

Для запуска бота в Телеграмм введите команду в терминале:
```commandline
python talking_bot.py
```
![teleg](https://user-images.githubusercontent.com/77689849/203843636-0f9eb5bb-264b-4a15-b05f-4d1c1eba1453.gif)

Для запуска бота Вконтакте:
```commandline
python vk_bot.py
```
![vk](https://user-images.githubusercontent.com/77689849/203844064-e82dcaa3-3387-4cfb-9c26-798411305aa3.gif)

Для тренировки бота запустите файл `bot_trainer.py`, указав путь к JSON файлу, как показано в примере:
```commandline
python bot_trainer.py --training_file путь_к_файлу
```
Пример JSON файла:
```json
{
  "Устройство на работу": {
    "questions": [
      "Как устроиться к вам на работу?",
      "Как устроиться к вам?",
      "Как работать у вас?",
      "Хочу работать у вас",
      "Возможно-ли устроиться к вам?",
      "Можно-ли мне поработать у вас?",
      "Хочу работать редактором у вас"
    ],
    "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
  }
}
```
