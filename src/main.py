import json
import os

from dotenv import load_dotenv
from spellbook import TEMPLATE
import requests

import openai

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class OpenAIChat:
    def __init__(self, api_key):
        self.history = [OpenAIChat._user_query(TEMPLATE)]
        openai.api_key = api_key

    def clean_history(self):
        self.history = [OpenAIChat._user_query(TEMPLATE)]

    def chat(self, user_message: str) -> str:
        # Append user message to history
        self.history.append(self._user_query(user_message))
        # Prepare the prompt
        prompt = "\n".join(self.history) + "\nAI:"

        # Send to OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose the model you prefer
            prompt=prompt,
            max_tokens=200  # Adjust based on your needs
        )

        ai_response = response.choices[0].text.strip()
        # Append AI's response to history
        self.history.append(f"AI: {ai_response}")

        return ai_response

    @staticmethod
    def _user_query(user_message):
        return f"User: {user_message}"


# pre-condition : llm_input contains "intent"
def process_intent(llm_output) -> str:
    intent = llm_output["intent"]
    if intent == "SEARCH":
        raw_query: str = llm_output["query"]
        query_elements = raw_query.split(" ")
        # curl -X 'GET' 'https://www.data.gouv.fr/api/1/datasets/?q=exports&q=armes&q=francais'
        # todo try catch la request
        response = requests.get(url=f"https://www.data.gouv.fr/api/1/datasets",
                                params={"q": query_elements})
        if response.ok:
            datasets = response.json()
            #  todo simplify simple_datasets
            simple_datasets = datasets
            return f"Here are the datasets we found: {simple_datasets}"
        else:
            return "Sorry, I'm having issues searching the dataset database"
        # do something
    elif intent == "GET_DATASET":
        raise NotImplementedError("failure of gpt to respect spec")
    else:
        return f"Unimplemented intent: {intent}"


def main() -> None:
    chat_session = OpenAIChat(api_key=OPENAI_API_KEY)
    do_stop = False
    message = "Je suis un assistant de data gouv. Je peux trouver des datasets.\n"
    while not do_stop:
        user_input = input(message)
        response = chat_session.chat(user_message=user_input)
        # todo try catch  llm output parsing
        llm_output: dict = json.loads(response)
        if "intent" in llm_output.keys():
            message = process_intent(llm_output)
            # for the moment: no memory between processed intents
            chat_session.clean_history()
        elif "direct_response" in llm_output.keys():
            message = llm_output["direct_response"]
            continue
        else:
            raise NotImplementedError


INTENT_TO_API_MAP = {
    "SEARCH": 'https://www.data.gouv.fr/api/1/datasets/?q=QUERY_TERM&page=1&page_size=20',
    "GET_DATASET": 'https://www.data.gouv.fr/api/1/datasets/DATASET_ID/',
}

if __name__ == "__main__":
    main()
