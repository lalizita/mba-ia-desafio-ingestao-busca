import os
from dotenv import load_dotenv
from typing import List
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

for var in ["DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "GOOGLE_API_KEY"]:
    if not os.getenv(var):
        raise RuntimeError(f"A variável de ambiente {var} não foi definida.")

# @DUVIDA AQUI: Por que preciso fazer embedding aqui de novo? Não bastaria usar o conteúdo criado na ingestão?
embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
vector_store = PGVector(
    connection=DATABASE_URL,
    collection_name=PG_VECTOR_COLLECTION_NAME,
    embeddings=embeddings
)

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join([doc.page_content for doc in docs])


def search_prompt() -> Runnable:
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL, temperature=0)

    rag_chain = (
        {"contexto": retriever | format_docs, "pergunta": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain
