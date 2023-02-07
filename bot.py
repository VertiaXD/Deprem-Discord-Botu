import requests
import discord
import datetime
import time
import asyncio
from earthquake_data import EarthquakeData

client = discord.Client(intents=discord.Intents.all())
TOKEN = "TOKEN"
CHANNEL_ID = "KANAL_ID"

# Her döngüden sonra beklenecek saniye sayısı
# Eğer hiç beklemezseniz site sizi kısa süreliğine banlıyor.
delay = 60

def get_earthquake_info_kandilli():
    url = 'https://api.orhanaydogdu.com.tr/deprem/live.php?limit=1'
    
    try:
        response = requests.get(url)
        
        # Eğer site hata döndürürse None döndür.
        if response.status_code != 200:
            return None
        
        data = response.json()
        earthquake_info = data['result'][0]
        
        eq_data = EarthquakeData(
            magnitude=earthquake_info['mag'],
            timestamp=earthquake_info['timestamp'],
            location=earthquake_info['lokasyon'],
            lat=earthquake_info['lat'],
            long=earthquake_info['lng'],
            depth=earthquake_info['depth'],
            hash=earthquake_info['hash'],
        )
        
        return eq_data
    except Exception as e:
        print(f'Bir hata meydana geldi: {e}')
        return None

def get_earthquake_info_usgs():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2023-01-01&endtime=2023-12-31&limit=1&orderby=time&latitude=39&longitude=35&maxradiuskm=1000"

    try:
        response = requests.get(url)
        
        # Eğer site hata döndürürse None döndür.
        if response.status_code != 200:
            return None
        
        data = response.json()
        earthquake_info = data['features'][0]
        
        eq_data = EarthquakeData(
            magnitude=earthquake_info['properties']['mag'],
            timestamp=earthquake_info['properties']['time'] // 1000,
            location=earthquake_info['properties']['place'],
            lat=earthquake_info['geometry']['coordinates'][0],
            long=earthquake_info['geometry']['coordinates'][1],
        )
        return eq_data
    except Exception as e:
        print(f'Bir hata meydana geldi: {e}')
        return None
    
@client.event
async def on_ready():
    print(f"Bot is ready, running on {client.user}")
    channel = client.get_channel(int(CHANNEL_ID))
    last_hash = None
    
    while True:
        eq_data = get_earthquake_info_kandilli()
        
        if eq_data is None:
            eq_data = get_earthquake_info_usgs()
            if eq_data is None:
                await asyncio.sleep(delay)
                continue
        
        if last_hash == eq_data.hash:
            await asyncio.sleep(delay)
            continue
        last_hash = eq_data.hash
        
        message = eq_data.get_message()
        
        await channel.send(message)
        await asyncio.sleep(delay)
        
client.run(TOKEN)
