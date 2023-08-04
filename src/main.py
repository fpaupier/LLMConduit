import os

from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","")

def main() -> None:
    llm = OpenAI(openai_api_key=OPENAI_API_KEY)
    res = llm.generate(["Propose me a brief history of France's medieval history in ten lines. Use the tone of a medieval bard and use rhymes"])
    print(res.generations[0])


if __name__ == "__main__":
    main()
