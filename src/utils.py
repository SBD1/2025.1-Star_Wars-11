def mostrar_menu(opcoes: list[str]) -> int:
    for i, opt in enumerate(opcoes, start=1):
        print(f"{i} — {opt}")
    escolha = input("Escolha uma opção: ")
    if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
        return int(escolha)
    print("Opção inválida, tente novamente.")
    return mostrar_menu(opcoes)
