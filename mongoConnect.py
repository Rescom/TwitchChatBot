import json
import urllib.parse
from pymongo import MongoClient

# Carrega as configuraçoes de config.json
def load_config():
    with open("config.json", 'r') as file:
        return json.load(file)

#Conectar ao MongoDB
def connect_to_mongodb():
    config = load_config()
    mongodb_config = config.get('mongodb', {})

    username = mongodb_config.get("username")
    password = mongodb_config.get("password")
    cluster = mongodb_config.get("cluster")

    if not username or not password or not cluster:
        raise ValueError("Configurações do MongoDB estão faltando. Por favor, configure-as no menu.")

    username = urllib.parse.quote_plus(username)
    password = urllib.parse.quote_plus(password)

    connection_string = f"mongodb+srv://{username}:{password}@{cluster}.cbqex.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)

    return client

#Salvando as mensagens no mongoDB
def save_message_to_db(client, message):
    db = client["twitch_bot"]  # Acessa o banco de dados 'twitch_bot'
    messages_collection = db["messages"]  # Acessa a colecao 'messages'
    #Estrutura do documento a ser inserido
    message_data = {
        "username": message.author.name,
        "content": message.content,
        "channel": message.channel.name,
        "timestamp": message.timestamp
    }

    # Inserindo o documento no mongoDB 
    messages_collection.insert_one(message_data)

