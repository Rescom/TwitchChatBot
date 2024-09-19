from twitchio.ext import commands
from colorama import Fore
from mongoConnect import connect_to_mongodb, save_message_to_db, load_config  # Importando a função load_config

class Bot(commands.Bot):
    def __init__(self):
        config = load_config()  # Carrega as configurações do arquivo config.json
        initial_channels = config.get("channels")  # Pega os canais configurados
        super().__init__(token="<twitchToken>", prefix="!", initial_channels=initial_channels)

        # Conecta ao MongoDB
        self.client = connect_to_mongodb()

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f"User Id is | {self.user_id}")

    async def event_message(self, message):
        if message.echo:
            return

        # Exibe a mensagem no terminal
        print(f"{Fore.CYAN}{message.author.name}:{Fore.WHITE}{message.content}")

        save_message_to_db(self.client, message)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"hello {ctx.author.name}!")
