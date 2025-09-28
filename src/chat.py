from search import search_prompt

def main() -> None:
    try:
        chain = search_prompt()
    except Exception as e:
        print(f"Erro ao inicializar a cadeia de busca: {e}")
        return

    print("Chat iniciado! Digite 'sair' para terminar.")
    while True:
        try:
            question = input("Sua pergunta: ")
            if question.lower() == 'sair':
                print("Encerrando o chat.")
                break
            if not question.strip():
                continue

            response = chain.invoke(question)
            print("\nResposta:", response)
            print("-" * 20)
        except KeyboardInterrupt:
            print("\nEncerrando o chat.")
            break
        except Exception as e:
            print(f"\nOcorreu um erro durante a busca: {e}")
            print("-" * 20)

if __name__ == "__main__":
    main()
