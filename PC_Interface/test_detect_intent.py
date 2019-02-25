import os

import time
from google.oauth2 import service_account

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(credentials_path)
PROJECT_ID = os.getenv('GCLOUD_PROJECT')

print('Credendtials from environ: {}'.format(credentials))


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    query_text = response.query_result.query_text
    intent = response.query_result.intent.display_name
    # confidence = response.query_result.intent_detection_confidence
    # fulfillment = response.query_result.fulfillment_text
    # parameters = response.query_result.parameters

    print('=' * 80)
    print('Query text: {}'.format(query_text))
    # print('Detected intent: {} (confidence: {})\n'.format(intent, confidence))
    # print('Fulfillment text: {}\n'.format(fulfillment))
    # print('Parameter Entity : {}'.format(parameters))

    return intent


if __name__ == '__main__':
    start = time.time()
    print(start)
    # lines = ['initialize integer variable named F with value 90',
    #          'add \'They are competetive\' to variable mal', 'assign 89.6 to variable rt',
    #          'find accuracy of model']
    full_corpus = open('/media/madusha/DA0838CA0838A781/PC_Interface/Resources/users_entered_lines')
    lines = [line for line in full_corpus.readlines() if line.strip()]
    for line in lines:
        detect_intent_texts(PROJECT_ID, 'df', line, 'en-US')

    end = time.time()
    print(end - start)
