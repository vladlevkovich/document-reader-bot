from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pprint import pprint
from .prompt import system_prompt
import os

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('key')

# завантаження документа
def load_document(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

# розбиття документа на частини
def split_document(doc):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(doc)
    return splits

# створення векторного середовища
def create_vector_store(splits):
    return Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# створення шаблону запиту
def create_prompt():
    return ChatPromptTemplate.from_messages(
        [
            ('system', system_prompt),
            ('human', '{input}')
        ]
    )

# ланцюг запитів
def create_rag_chain(retriever, prompt, llm):
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)

# обробка запиту
def process_document(file_path, query):
    doc = load_document(file_path)
    splits = split_document(doc)
    vectorstore = create_vector_store(splits)
    retriever = vectorstore.as_retriever()

    prompt = create_prompt()
    llm = ChatOpenAI(model='gpt-4o')
    rag_chain = create_rag_chain(retriever, prompt, llm)
    results = rag_chain.invoke({'input': query})
    return results['answer']

# loader = PyPDFLoader('../files/test.pdf')
# doc = loader.load()
#
# llm = ChatOpenAI(model='gpt-4o')
#
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(doc)
# vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
# retriever = vectorstore.as_retriever()
#
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ('system', system_prompt),
#         ('human', '{input}')
#     ]
# )
#
# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)
# results = rag_chain.invoke({'input': 'Based on this document, make a general conclusion'})
# # results = rag_chain.invoke({'input': 'What this document is about'})
#
# print(results)
# print(results['answer'])
