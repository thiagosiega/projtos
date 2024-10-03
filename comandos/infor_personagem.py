from main import GemineApp
import genai

# Inicializa o modelo
model = genai.GenerativeModel("gemini-1.5-flash")
app = GemineApp()

# Caminho para o arquivo do personagem
FILE_PERSONAGEM = "personagem.txt"

def get_character_info():
    """Exibe informações sobre um personagem de anime."""
    try:
        with open(FILE_PERSONAGEM, "r") as file:
            personagem = file.read()
        return personagem
    except FileNotFoundError:
        return "Arquivo de personagem não encontrado."

def add_info_to_response(response):
    """Adiciona informações do personagem à resposta."""
    character_info = get_character_info()
    return f"{response}\n\n{character_info}"

def execute_action(action, response=""):
    """Executa a ação correspondente à resposta."""
    if action == "get_character_info":
        return get_character_info()
    elif action == "add_info_to_response":
        return add_info_to_response(response)
    else:
        return "Ação inválida."

def main():
    """Mostra informações sobre a área dedicada ao personagem."""
    info_messages = [
        "Essa área é dedicada ao personagem.",
        "Comandos disponíveis: get_character_info, add_info_to_response.",
        "Local onde você pode adicionar informações sobre o personagem para melhorar a resposta."
    ]
    
    # Exibe informações iniciais
    for message in info_messages:
        print(message)
    
    # Loop para interação do usuário
    while True:
        action = input("Digite um comando (ou 'sair' para encerrar): ").strip()
        
        if action.lower() == 'sair':
            print("Saindo...")
            break
        
        response = input("Digite a resposta (ou deixe em branco para apenas obter informações): ").strip()
        
        # Executa a ação e obtém o resultado
        result = execute_action(action, response)
        print(result)  # Exibe a resposta ou informações

if __name__ == "__main__":
    main()
