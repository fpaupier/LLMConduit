import json
import os

from dotenv import load_dotenv
from spellbook import TEMPLATE
import requests

import openai

from src.utils import fetch_data_with_retries

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
    def _user_query(user_message: str) -> str:
        return f"User: {user_message}"


# pre-condition : llm_input contains "intent"
def process_intent(llm_output: dict) -> str:
    intent = llm_output["intent"]
    if intent == "SEARCH":
        raw_query: str = llm_output["query"]
        query_elements = raw_query.split(" ")
        params = {"q": query_elements}
        success, datasets = fetch_data_with_retries(url="https://www.data.gouv.fr/api/1/datasets",params=params)
        if success:
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
    message = ("Hello! Vous voulez explorer le catalogue des données publiques sur data.gouv.fr? Je suis là pour vous "
               "aider.\nQue désirez-vous faire?\n")
    do_stop = False
    while not do_stop:
        user_input = input(message)
        response = chat_session.chat(user_message=user_input)
        llm_output: dict = parse_llm_output(response)
        if "intent" in llm_output.keys():
            message = process_intent(llm_output)
            # for the moment: no memory between processed intents
            chat_session.clean_history()
        elif "direct_response" in llm_output.keys():
            message = llm_output["direct_response"]
        elif "error" in llm_output.keys():
            message = "Je n'ai pas compris votre question. Pouvez-vous ré-essayer?"


def parse_llm_output(llm_output: str) -> dict:
    """
    :param llm_output: the output of the LLM that is expected to be a valid JSON
    :return: proper python dictionary based on the llm output.
    """
    try:
        json_output = json.loads(llm_output)
        return json_output
    except json.decoder.JSONDecodeError:
        return {"error": "failed to parse llm output"}
    except Exception as e:
        return {"error": f"unknown error {e}"}


if __name__ == "__main__":
    main()
