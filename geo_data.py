import os
import pandas as pd
import geoip2.database
import re

# GeoIP veritabanının yolunu belirtin
geoip_db_path = "geoip_db_path"

# GeoIP Reader'ı oluşturun
try:
    reader = geoip2.database.Reader(geoip_db_path)
    print(f"GeoIP database loaded successfully from: {geoip_db_path}")
except FileNotFoundError:
    print(f"GeoIP database not found at: {geoip_db_path}")
    print("Please make sure you've placed the GeoLite2-City.mmdb file in the correct directory.")
    reader = None

# Log dosyasının yolunu belirtin
log_file_path = 'log_path'  

# Log dosyasını okuyup IP adreslerini çıkartın
ip_addresses = []
with open(log_file_path, 'r') as file:
    for line in file:
        # IP adreslerini çıkartmak için regex kullanın
        match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)
        if match:
            ip_addresses.append(match.group())

# IP adreslerini DataFrame'e yükleyin
df = pd.DataFrame(ip_addresses, columns=['ip'])

# Coğrafi bilgi ekleme fonksiyonu
def add_geo_info(ip):
    if reader:
        try:
            response = reader.city(ip)
            return response.country.name
        except geoip2.errors.AddressNotFoundError:
            return "Unknown"
    return "GeoIP database not available"

# IP adreslerine göre ülke bilgilerini ekleyin
df['country'] = df['ip'].apply(add_geo_info)

# İşlenen veriyi kaydedin
df.to_csv('C:\\Users\\syorg\\output.csv', index=False)
import pandas as pd

# CSV dosyasını yükleyin
csv_file_path = 'csv_file_path'  
df = pd.read_csv(csv_file_path)

# "Unknown" içeren satırları filtreleyin
df_filtered = df[df['country'] != 'Unknown']

# Filtrelenmiş veriyi yeni bir CSV dosyasına kaydedin
filtered_csv_file_path = 'filtered_csv_file_path'
df_filtered.to_csv(filtered_csv_file_path, index=False)

print(f"Filtered CSV file saved to: {filtered_csv_file_path}")
