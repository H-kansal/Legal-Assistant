from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()


def getLLM():
    llm = ChatOpenAI(
        model="groq-openai",  
        base_url=os.getenv("LITELLM_URI"),
        api_key="dummy",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}}
    )
    return llm