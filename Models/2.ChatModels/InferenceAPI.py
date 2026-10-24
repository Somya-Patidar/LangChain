from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pathlib import Path
import os

#only if env is some other folder not needed here
env_path= Path(__file__).resolve().parent.parent /"Models"/".env"
load_dotenv(env_path)

llm=HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    provider="featherless-ai",
    huggingfacehub_api_token=os.environ["HF_TOKEN"]
)

model=ChatHuggingFace(llm=llm)