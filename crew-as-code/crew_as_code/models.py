from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

GROQ_8B = "llama3-8b-8192"
GROQ_70B = "llama3-70b-8192"
MIXTRAL = "mixtral-8x7b-32768"
GEMMA = "gemma-7b-it"
GPT4O = "gpt-4o"
GPT3TURBO = "gpt-3.5-turbo-0125"

class LLM:

    def __init__(self, groq_api_keys:list[str]):
        self.groq_api_keys = groq_api_keys
        self.groq_8b = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=GROQ_8B, temperature=0.2)
        self.groq_70b = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=GROQ_70B, temperature=1)
        self.mixtral = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=MIXTRAL,temperature=0.3)
        self.gemma = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=GEMMA,temperature=0.3)
        self.gpt4o = lambda: ChatOpenAI(model=GPT4O,temperature=0.3)
        self.gpt3turbo = lambda: ChatOpenAI(model=GPT3TURBO,temperature=0.3)


    def get_groq_api_key(self):
        key = self.groq_api_keys[0]
        self.groq_api_keys = self.groq_api_keys[1:] + [key]
        return key
