from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
load_dotenv()

os.environ['HUGGINGFACEHUB_API_TOKEN']='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'

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"
)

# add_routes(
#     app,
#     ChatOpenAI(),
#     path="/openai"
# )
# model=ChatOpenAI()
##ollama llama2
llm=Ollama(model="brutus-no-sys")
#llm=HuggingFaceHub(repo_id="maniacamit/CodeLlama-7b-Instruct-hf-finetuned", model_kwargs={"temperature":0, "max_length":64})
prompt1=ChatPromptTemplate.from_template("You are a DevOps Consutant in OneShop provide details {topic}")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 5 years child with 100 words")

add_routes(
    app,
    prompt1|llm,
    path="/oneshopinfo"
)

add_routes(
    app,
    prompt2|llm,
    path="/onebbinfo"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)
