from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain 


load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ['HUGGINGFACEHUB_API_TOKEN']='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'


## Prompt Template

# template = """<s>[INST]{question}[/INST]"""
# prompt = PromptTemplate.from_template(template=template)
prompt=ChatPromptTemplate.from_messages(
    ["""<s>[INST]{question}[/INST]"""]
)
## streamlit framework  

st.title('Let\'s Test Brutus')
input_text=st.text_input("I am still in development please be gentle :)")

# ollama LLAma2 LLm 
#llm=Ollama(model="brutus")
llm = Ollama(model="brutus")
#llm=HuggingFaceHub(repo_id="maniacamit/CodeLlama-7b-Instruct-hf-finetuned", model_kwargs={"temperature":0, "max_length":64})
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))