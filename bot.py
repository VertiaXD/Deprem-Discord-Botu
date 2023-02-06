import requests
import discord

client = discord.Client(intents=discord.Intents.all())


TOKEN = "TOKEN"

CHANNEL_ID = "KANAL ID"

url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-01-01&endtime=2023-12-31&minmagnitude=4&limit=1&orderby=time&latitude=39&longitude=35&maxradiuskm=1000"

def get_earthquake_info():
    response = requests.get(url)
    data = response.json()
    earthquake_info = data['features'][0]['properties']
    return earthquake_info

@client.event
async def on_ready():
    print(f"Bot is ready, running on {client.user}")
    channel = client.get_channel(int(CHANNEL_ID))
    earthquake_info = get_earthquake_info()
    message = f"**DİKKAT! TÜRKİYEDE DEPREM!!!:**\nBüyüklük: {earthquake_info['mag']}\nLokasyon: {earthquake_info['place']}\nZaman: {earthquake_info['time']}\nDetaylı Bilgi: {earthquake_info['url']}"
    await channel.send(message)

client.run(TOKEN)
