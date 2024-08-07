from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

CLAUDE_SONNET_35 = "claude-3-5-sonnet-20240620"
GROQ_8B = "llama3-8b-8192"
GROQ_70B = "llama3-70b-8192"
MIXTRAL = "mixtral-8x7b-32768"
GEMMA = "gemma-7b-it"
GPT4O = "gpt-4o"
GPT3TURBO = "gpt-3.5-turbo-0125"
GPT4OMINI= "gpt-4o-mini"

class LLM:

    def __init__(self, groq_api_keys:list[str]):
        self.groq_api_keys = groq_api_keys
        self.groq_8b = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=GROQ_8B, temperature=0.2)
        self.groq_70b = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=GROQ_70B, temperature=1)
        self.mixtral = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=MIXTRAL,temperature=0.3)
        self.gemma = lambda: ChatGroq(groq_api_key=self.get_groq_api_key(), model_name=GEMMA,temperature=0.3)
        self.claude35 = lambda: ChatAnthropic(model=CLAUDE_SONNET_35,temperature=0.3)

    def gpt4o(self, temperature:float=0.3):
        return ChatOpenAI(model=GPT4O,temperature=temperature)
    
    def gpt4omini(self, temperature:float=0.3):
        return ChatOpenAI(model=GPT4OMINI,temperature=temperature)
    
    def gpt3turbo(self, temperature:float=0.3):
        return ChatOpenAI(model=GPT3TURBO,temperature=temperature)

    def get_groq_api_key(self):
        key = self.groq_api_keys[0]
        self.groq_api_keys = self.groq_api_keys[1:] + [key]
        return key
