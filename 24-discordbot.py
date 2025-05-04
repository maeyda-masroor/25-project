import discord
import os
import requests
import json
import random
import re
from discord.ext import commands
from dotenv import load_dotenv


# pip install -U discord.py
# pip install python-dotenv

#maeydahmasroor@Maeydahs-MacBook-Pro ~ % source venv/bin/activate

def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        json_data = json.loads(response.text)
        
        if json_data and isinstance(json_data, list) and len(json_data) > 0:
            return f'"{json_data[0]["q"]}" - {json_data[0]["a"]}'
        return "Could not fetch a quote at this time."
    
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Sorry, I couldn't fetch a quote right now."

load_dotenv()
token = os.getenv("Token")

if not token:
    raise ValueError("TOKEN environment variable not set. Please check your .env file.")

#intents = discord.Intents.default()
#intents.message_content = True

#bot = commands.Bot(command_prefix="!", intents=intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = [
    "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
    "lonely"
]

starter_encouragements = [
    "Cheer up!",
    "Hang in there!",
  	"You great person"
  ]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Convert message to lowercase and remove punctuation for better matching
    msg = re.sub(r'[^\w\s]', '', message.content.lower())
    
    if message.content.startswith("$inspire"):
        async with message.channel.typing():
            await message.channel.send(get_quote())
    
    # Check for whole words only
    if any(re.search(rf'\b{word}\b', msg) for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

client.run(token)