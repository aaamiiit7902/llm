from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.retrievers import ParentDocumentRetriever

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

from langchain.prompts import ChatPromptTemplate
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi import FastAPI
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain.schema import StrOutputParser
import uvicorn

llm = Ollama(model="brutus-no-sys")
bge_embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5", 
encode_kwargs={"normalize_embeddings": True})

loaders =  [
    TextLoader("./data/data.txt")
]
docs = []
for l in loaders:
    docs.extend(l.load())
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

child_splitter = RecursiveCharacterTextSplitter(chunk_size=200)
vectorstore = Chroma(collection_name="split_parents", embedding_function=bge_embeddings)

# The storage layer for the parent documents
store = InMemoryStore()

big_chunks_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

big_chunks_retriever.add_documents(docs)

qa = RetrievalQA.from_chain_type(llm = llm,
                                 chain_type="stuff",
                                 retriever=big_chunks_retriever)

# query = "what is inventory service that is used in oneshop?"
# qa.run(query)



app = FastAPI(
    title="I am here to Serve Brutus",
    description="Endpoints of Brutus to be used in your application"
)
prompt_template = """You are an AI assistant created by Brutus, Use the provided context to answer the user question. If you don't know the answer, just say you don't know

Context:
{context}

Question:
{question}"""

rag_prompt = ChatPromptTemplate.from_template(prompt_template)

entry_point_chain=RunnableParallel(
    {"context": big_chunks_retriever , "question": RunnablePassthrough()}
)
rag_chain = entry_point_chain| rag_prompt | llm | StrOutputParser()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, rag_chain, path="/brutus")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)