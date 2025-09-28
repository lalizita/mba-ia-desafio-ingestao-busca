# Desafio MBA: Sistema de RAG com PGVector e Gemini

Este projeto implementa um sistema de Geração Aumentada por Recuperação (RAG - Retrieval-Augmented Generation). Ele utiliza o **PGVector** como banco de dados vetorial para armazenar o conteúdo de um documento PDF e o **Google Gemini** como modelo de linguagem para responder perguntas com base nesse conteúdo.

## Funcionalidades

- **Ingestão de PDF**: Processa um arquivo PDF, divide-o em partes (chunks) e gera embeddings para cada parte.
- **Armazenamento Vetorial**: Salva os embeddings no PostgreSQL com a extensão PGVector.
- **Busca por Similaridade**: Recupera os trechos mais relevantes do documento com base na pergunta do usuário.
- **Geração de Resposta**: Utiliza o modelo Gemini para gerar uma resposta coesa e precisa, usando os trechos recuperados como contexto.

## Pré-requisitos

- Python 3.9+
- Docker e Docker Compose
- Uma chave de API do [Google AI Studio](https://aistudio.google.com/app/apikey).

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd mba-ia-desafio-ingestao-busca
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # No Windows, use: venv\Scripts\activate
    ```

3.  **Instale as dependências do Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Suba o banco de dados com Docker:**
    O projeto necessita de uma instância do PostgreSQL com a extensão PGVector. Você pode usar o `docker-compose.yml` na raiz do projeto (se não existir, crie um com o conteúdo do exemplo no repositório).
    ```bash
    docker-compose up -d
    ```

5.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto, copiando o `.env.example`. Preencha com suas informações:
    ```env
    # Chave de API obtida no Google AI Studio
    GOOGLE_API_KEY="sua_chave_de_api_aqui"

    # String de conexão com o banco de dados Docker (atenção a porta que sobe o container)
    DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5433/rag"

    # Nome da coleção (tabela) que será criada no PGVector
    PG_VECTOR_COLLECTION_NAME="rag"

    # Caminho para o arquivo PDF que será ingerido
    PDF_PATH="document.pdf"
    ```
    **Importante:** Certifique-se de que o arquivo PDF exista no caminho especificado.

## Como Executar

1.  **Ingestão dos Dados (Vetorização):**
    Este comando irá ler o PDF, processá-lo e armazenar os vetores no banco de dados. O processo apaga a coleção antiga para garantir que os dados estejam sempre atualizados.
    ```bash
    python src/ingest.py
    ```

2.  **Inicie o Chat:**
    Após a ingestão ser concluída com sucesso, execute o script de chat para começar a fazer perguntas baseadas no conteúdo do seu PDF.
    ```bash
    python src/chat.py
    ```
    O terminal exibirá a mensagem `Chat iniciado! Digite 'sair' para terminar.` e aguardará sua pergunta.

