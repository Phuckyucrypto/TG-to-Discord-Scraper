import os
import asyncio
import ssl
import certifi
from dotenv import load_dotenv
from telethon import TelegramClient, events
import discord
from discord.ext import commands
from aiohttp import TCPConnector

# Load environment variables
load_dotenv()

# Telegram setup
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE')
telegram_client = TelegramClient(phone_number, api_id, api_hash)

# Create an SSL context using certifi's certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Discord setup
discord_token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.messages = True

# Configure the Discord bot to use the SSL context with the certifi CA file
discord_client = commands.Bot(command_prefix='!', intents=intents, connector=TCPConnector(ssl=ssl_context))

# Discord channel ID where messages will be forwarded
discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')

async def send_to_discord(message):
    channel = discord_client.get_channel(int(discord_channel_id))
    if channel:
        await channel.send(message)

@telegram_client.on(events.NewMessage(chats=-1001730427571))
async def handle_new_message(event):
    message_content = f"New message from {event.sender_id}: {event.message.text}"
    await send_to_discord(message_content)

async def main():
    print("Starting Telegram client...")
    await telegram_client.start()
    print("Telegram client started successfully.")
    
    print("Starting Discord client...")
    await discord_client.start(discord_token)
    print("Discord client started successfully.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


