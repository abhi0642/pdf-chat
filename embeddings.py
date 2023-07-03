import PyPDF2
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
import getpass
import os
from langchain.vectorstores import Weaviate
import weaviate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


os.environ["OPENAI_API_KEY"] = \
    "ENTER YOUR KEY HERE"
pdf_path = "NIPS-2017.pdf"
WEAVIATE_URL = getpass.getpass(
    "ENTER YOUR WEAVIATE URL HERE")
WEAVIATE_API_KEY = getpass.getpass(
    "ENTER YOUR WEAVIAE API KEY HERE")
auth_config = weaviate.AuthApiKey(
    api_key=WEAVIATE_API_KEY)
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config
)


def create_and_store_embeddings():
    with open(pdf_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)

            embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
            text_embeddings=embeddings.embed_query(text=text)
            db = Weaviate.from_texts(
                texts=chunks,
                embedding=embeddings,
                weaviate_url=WEAVIATE_URL,
                client=client,
                by_text=False
            ).as_retriever()
            return db


def return_response(query,db):
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    docs = db.get_relevant_documents(query)
    return chain.run(input_documents=docs, question=query)
