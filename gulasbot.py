import os
import random
import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import json
#nn vo botar as api key nem adicionar um txr com nada to com um pouco de preguiça 
GIPHY_API_KEY = ""

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
client = commands.Bot(command_prefix='?', intents=intents)


#lista do que ele fala '-'
say = [

]

@client.event
async def on_ready():
    print(f'{client.user} online')
@client.command(name='oi')
async def send_random_meme(ctx):
    response = get_random_meme()
    await ctx.send(response)

@client.command(name='prune')
async def clear_messages(ctx, amount=5):
    if amount > 100:
        await ctx.send("só pode ate 100 '-'")
        return
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} mensagens apagadas")

@client.command()
async def gif(ctx, *, query):
    url = f'https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={query}&limit=100'
    response = requests.get(url)
    data = response.json()
    
    if len(data['data']) > 1:
        randomgif = random.randint(0, len(data['data'])-1)
        gif_url = data['data'][randomgif]['images']['original']['url']
        await ctx.send(gif_url)
    else:
        await ctx.send(f"não existe gif de {query}")
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if any(word in message.content.lower() for word in say):
        #chance de 10% de enviar um gif eu acho nn sou o melhor em matematica
        if random.random() < 0.10:
            gif = get_random_gif()
            if gif:
                await message.channel.send(gif)
        #chance de 20% de enviar uma mensagem aleatória
        elif random.random() < 0.20:
            response = get_random_meme()
            await message.channel.send(response)
    await client.process_commands(message)


def get_random_meme():
    return random.choice(say)
def get_random_gif():
    #chave do giphy
    api_key = ''
#palavra que ele pesquisa \/
    query = "kitten"
    url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=100"
    response = requests.get(url)
    if response.ok:
        data = response.json()['data']
        if data:
            gif = random.choice(data)
            return gif["images"]["original"]["url"]
    return None

#token aqui
DISCORD_TOKEN = ""

client.run(DISCORD_TOKEN)