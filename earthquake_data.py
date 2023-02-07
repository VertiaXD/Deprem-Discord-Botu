import hashlib
import datetime

# Deprem bilgilerini tutan bir class
class EarthquakeData():
    def __init__(self, magnitude=None, timestamp=None, date=None, time=None, location=None, lat=None, long=None, depth=None, hash=None) -> None:
        self.md5 = hashlib.md5()
        
        self.magnitude = magnitude
        self.timestamp = timestamp
        self.location = location
        self.date = date
        self.time = time
        self.lat = lat
        self.long = long
        self.depth = depth
        self.hash = hash
        
        if self.date is None or self.time is None:
            self.create_date_and_time()
        
        if self.hash is None:
            self.create_hash()
        
        
    def create_date_and_time(self):
        earthquake_time = datetime.datetime.fromtimestamp(self.timestamp)
        
        # Tarih ve saati yazdırabilmek için
        self.date = earthquake_time.strftime('%Y/%m/%d')
        self.time = earthquake_time.strftime('%H:%M:%S')
    
    # Farklı API'lar farklı sonuçlar döndürdüğünden böyle bir çözüm geliştirdim
    # Sadece gelen verileri ekrana yazdırıyor.
    def get_message(self):
        variables = vars(self)
        
        keys_to_iterate = [
            'magnitude',
            'location',
            'depth',
            'lat',
            'long',
            'date',
            'time'
        ]
        key_to_str = {
            'magnitude': 'Büyüklük',
            'location': 'Lokasyon',
            'lat': 'Enlem',
            'long': 'Boylam',
            'depth': 'Derinlik',
            'date': 'Tarih',
            'time': 'Zaman',
        }
        
        message = "**TÜRKİYE'DE DEPREM**\n"
        for key in keys_to_iterate:
            if variables[key] is None:
                continue
            message += '{}: {}\n'.format(key_to_str[key], variables[key])
        return message
    
    # Hash oluşturur. Aldığımız iki deprem bilgisinin aynı olup olmadığını anlamamızı sağlar
    def create_hash(self):
        variables = vars(self)
        all_str = '{magnitude}{timestamp}{location}{lat}{long}{depth}'.format(**variables)
        self.md5.update(all_str.encode('UTF-8'))
        self.hash = self.md5.hexdigest()

