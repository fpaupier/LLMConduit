import json
import os

from dotenv import load_dotenv
from spellbook import TEMPLATE

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
            process_intent()
        elif "direct_response" in json_output.keys():
            print(json_output["direct_response"])
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

# CONTEXT PROMPT
# You provide a text interface for an API. There are 2 different intents: search a dataset (intent=SEARCH) and
# get information for a dataset (intent=GET_DATASET)
# I will provide you with user requests in this format:
# USER_REQUEST: <the user request text>
# Then you will read the USER_REQUEST and answer in json format. See examples below.
#
# The api provides a list of datasets. It is possible to search through datasets and get information about a dataset.
# You have to detect between 2 different intents:
# SEARCH: when the user wants to search available datasets for a given topic
# GET_DATASET: when the user wants to get information about a specific topic
#
# For SEARCH, you will have to understand what would be a good search query based on the user request.
# For instance: if the input is
# USER_REQUEST: trouve les datasets au sujet de vélos
# You should output in json format:
# {"intent":SEARCH, "query": <velo>}
# If you detect the intent is SEARCH, but don't have the full context and need to pursue the conversation, for instance
# to get a search query, you should tell me you want to answer to the user directly by returning the following:
# {"direct_response": "<the response you want to give to the user to make progress>"}
# NOTE: the USER_REQUEST will be in French. The dataset names may be in French too.
#
# For GET_DATASET, you will have to understand what is the dataset you need to get. For instance, this is
# not implemented, so you can just answer.
# {"direct_response": "Getting a dataset is not implemented yet."}
#
# If you think the intent is neither GET_DATASET neither SEARCH, you should re-explain to the user
# the goal of this service and continue the conversation. You can tell me what you want to answer to
# the user by returning json format:
# {"direct_response": "<your answer to the user>"}


# TODO quand la demande est hors-contexte, utiliser un message hardcodé