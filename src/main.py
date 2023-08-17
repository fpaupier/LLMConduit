import json
import os

from dotenv import load_dotenv
from spellbook import template

import openai

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

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


def process_intent(param):
    print(param.intent)


def parse_llm_output(llm_output: str):
    print(f"Parsing llm output... ")
    try:
        json_output = json.loads(llm_output)
        if "intent" in json_output.keys():
            print(json_output.intent)
    except ValueError as e:
        pass  # invalid json
    else:
        pass  # valid json

    return

user_input = "Donne moi des jeux de données sur la consommation des ménages "

def main() -> None:
    chat_session = OpenAIChat(api_key=OPENAI_API_KEY)
    response = chat_session.chat(user_message=user_input)
    print(f"AI: {response}")

    ##
    #
    # llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    # prompt = PromptTemplate(template=template, input_variables=["question"])
    # llm_chin = LLMChain(prompt=prompt, llm=llm)
    # questioan = "USER_REQUEST: Donne moi un dataset sur la consommation des ménages français"
    # answer = llm_chain.run(question)
    # print(answer)
    # parse_llm_output(answer)
    # res = llm.generate(["Propose me a brief history of France's medieval history in ten lines. Use the tone of a medieval bard and use rhymes"])
    # print(res.generations[0])




INTENT_TO_API_MAP = {
    "SEARCH": 'https://www.data.gouv.fr/api/1/datasets/?q=QUERY_TERM&page=1&page_size=20',
    "GET_DATASET": 'https://www.data.gouv.fr/api/1/datasets/DATASET_ID/',
}


if __name__ == "__main__":
    main()
