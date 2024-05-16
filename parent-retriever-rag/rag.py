from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.retrievers import ParentDocumentRetriever

## Text Splitting & Docloader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.storage import InMemoryStore
from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
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
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
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



app = FastAPI()
prompt_template = """\
Use the provided context to answer the user question. If you don't know the answer, just say you don' know

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

add_routes(app, rag_chain, path="/rag")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)