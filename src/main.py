import json
import os

from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv
from spellbook import template

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

user_input = "Help me use the "

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

def main() -> None:
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    question = "USER_REQUEST: Donne moi un dataset sur la consommation des ménages français"
    answer = llm_chain.run(question)
    print(answer)
    parse_llm_output(answer)
    # res = llm.generate(["Propose me a brief history of France's medieval history in ten lines. Use the tone of a medieval bard and use rhymes"])
    # print(res.generations[0])




INTENT_TO_API_MAP = {
    "SEARCH": 'https://www.data.gouv.fr/api/1/datasets/?q=QUERY_TERM&page=1&page_size=20',
    "GET_DATASET": 'https://www.data.gouv.fr/api/1/datasets/DATASET_ID/',
}


if __name__ == "__main__":
    main()
