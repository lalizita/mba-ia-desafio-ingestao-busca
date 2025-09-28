import os
from dotenv import load_dotenv
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document

load_dotenv()
PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")

for var in ["PDF_PATH", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "GOOGLE_API_KEY"]:
    if not os.getenv(var):
        raise RuntimeError(f"A variável de ambiente {var} não foi definida.")


def ingest_pdf() -> None:
    """
    Carrega um documento PDF, o divide em partes (chunks), gera os embeddings
    e os armazena em um banco de dados PGVector.

    O processo é idempotente: a coleção existente é apagada antes da nova ingestão
    para evitar duplicatas e garantir que o banco de dados reflita apenas o
    conteúdo atual do PDF.
    """
    print(f"Iniciando a ingestão do PDF: {PDF_PATH}")

    loader = PyPDFLoader(PDF_PATH)
    docs: List[Document] = loader.load()
    print(f"Documento carregado com {len(docs)} página(s).")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)
    print(f"Documento dividido em {len(splits)} chunks para vetorização.")

    print(f"Inicializando o modelo de embeddings: {GOOGLE_EMBEDDING_MODEL}")
    embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)

    print(f"Armazenando {len(splits)} chunks na coleção '{PG_VECTOR_COLLECTION_NAME}'...")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        pre_delete_collection=True,
    )
    vector_store.add_documents(splits)

    print("\nIngestão concluída com sucesso!")


if __name__ == "__main__":
    ingest_pdf()