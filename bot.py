import json
import os
import sys
from twitchio.ext import commands
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
from colorama import Fore, Style, init
import getpass

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
    while True:
        clear_screen()  # Limpar o terminal antes de exibir o menu
        # Exibir a arte ASCII do logo da Twitch antes do menu
        print(twitch_ascii)
        
        config = load_config()
        
        print("\n---- Menu ----")
        print("1. Selecionar canal da Twitch")
        print("2. Configurar MongoDB (usuário, senha, cluster)")
        print("3. Iniciar o Bot")
        print("4. Sair")        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            # Configurar canais da Twitch
            channels = input("Digite o(s) nome(s) do(s) canal(is) da Twitch (separados por vírgula): ").split(',')
            config['channels'] = [channel.strip() for channel in channels]
            save_config(config)
            print(f"Canais da Twitch configurados: {config['channels']}")
            input("Pressione Enter para continuar...")
        
        elif choice == "2":
            # Configurar MongoDB
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
            print("Iniciando o Bot...")
            break  # Encerra o programa completamente
        
        elif choice=="4":
            print("Saindo do Programa...")
            sys.exit()                                           
        
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

# Classe do bot
class Bot(commands.Bot):
    def __init__(self):
        config = load_config()
        initial_channels = config.get("channels")
        super().__init__(token="<twitch_token>", prefix="!", initial_channels=initial_channels)

    async def event_ready(self):
        clear_screen()  # Limpar o terminal quando o bot estiver pronto
        print(twitch_ascii)
        print(f'Logged in as | {self.nick}')
        print(f"User Id is | {self.user_id}")

    async def event_message(self, message):
        if message.echo:
            return
        print(f"{Fore.CYAN}{message.author.name}: {message.content}")
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"hello {ctx.author.name}!")

# Programa principal
if __name__ == "__main__":
    # Exibe o menu e permite que o usuário configure as opções
    menu()
    
    # Carregar configurações e iniciar o bot
    bot = Bot()
    bot.run()
