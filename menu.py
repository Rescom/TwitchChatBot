import json
import os
import sys
import getpass
from colorama import Fore, init

# Inicializando colorama para cores no terminal
init(autoreset=True)

# Arte em ASCII com cor magenta
twitch_ascii = f"""
{Fore.MAGENTA}
   ███████████████████████████████████████████████
  ████████████████████████████████████████████████
  ██████                                     █████
 ███████                                     █████
████████                                     █████
████████                                     █████
████████                                     █████
████████            █████        █████       █████
████████            █████        █████       █████
████████            █████        █████       █████
████████            █████        █████       █████
████████            █████        █████       █████
████████            █████        █████       █████
████████            █████        █████       █████
████████            █████        █████       █████
████████                                     █████
████████                                    ██████
████████                                  ███████ 
████████                                ███████   
████████                               ██████     
██████████████████      ████████████████████      
██████████████████    ████████████████████        
██████████████████  ████████████████████          
██████████████████ ███████████████████            
            ██████████████                        
            ████████████                          
            ██████████                            
            ████████                              
"""


# Função para carregar configurações de arquivo JSON
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", 'r') as file:
            return json.load(file)
    else:
        return {"channels": [], "mongodb": {}}

# Função para salvar configurações em arquivo JSON
def save_config(config):
    with open("config.json", 'w') as file:
        json.dump(config, file, indent=4)

# Função para limpar o terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para o menu de configuração
def menu():
    from app import Bot  # Importar Bot aqui para evitar importações circulares
    while True:
        clear_screen()  # Limpar o terminal antes de exibir o menu
        print(twitch_ascii)  # Exibir a arte ASCII do logo da Twitch
        
        config = load_config()  # Carregar as configurações existentes do arquivo
        
        print("\n---- Menu ----")
        print("1. Selecionar canal da Twitch")
        print("2. Configurar MongoDB (usuário, senha, cluster)")
        print("3. Iniciar o bot")
        print("4. Sair")
        
        choice = input("Escolha uma opção: ")

        if choice == "1":
            channels = input("Digite o(s) nome(s) do(s) canal(is) da Twitch (separados por vírgula): ").split(',')
            config['channels'] = [channel.strip() for channel in channels]
            save_config(config)
            print(f"Canais da Twitch configurados: {config['channels']}")
            input("Pressione Enter para continuar...")

        elif choice == "2":
            username = input("Digite o usuário do MongoDB: ")
            password = getpass.getpass("Digite a senha do MongoDB: ")
            cluster = input("Digite o cluster do MongoDB: ")
            config['mongodb'] = {
                "username": username,
                "password": password,
                "cluster": cluster
            }
            save_config(config)
            print(f"Configurações do MongoDB salvas.")
            input("Pressione Enter para continuar...")

        elif choice == "3":
            print("Iniciando o bot...")
            bot = Bot()  # Instancia o bot
            bot.run()  # Inicia o bot com as configurações providas

        elif choice == "4":
            print("Saindo...")
            sys.exit()  # Encerra o programa completamente

        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    menu()
