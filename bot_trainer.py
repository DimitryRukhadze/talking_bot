import json
import argparse
import logging

from environs import Env

from google.cloud import dialogflow, dialogflow_v2beta1


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logging.info("Intent created: {}".format(response))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--training_file')
    args = parser.parse_args()

    env = Env()
    env.read_env()

    gcloud_project_id = env('GOOGLE_CLOUD_PROJECT_ID')

    with open(args.training_file, 'r', encoding='utf-8') as file:
        training_file_json = file.read()

    training_cases = json.loads(training_file_json)

    for case in training_cases:
        display_name = case
        case_body = training_cases[case]

        create_intent(
            gcloud_project_id,
            display_name,
            case_body['questions'],
            {case_body['answer']}
        )
