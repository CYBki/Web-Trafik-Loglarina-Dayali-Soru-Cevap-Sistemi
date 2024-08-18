import pandas as pd
import numpy as np
from datetime import datetime
import re
from user_agents import parse
from collections import defaultdict
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

# Log dosyasını işleme
def parse_log_line(line):
    # Bu regex örnek bir Apache Combined Log Format için tasarlanmıştır
    # Gerçek log formatınıza göre ayarlamanız gerekebilir
    pattern = r'(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(pattern, line)
    if match:
        ip, _, _, timestamp, request, status, bytes_size, referrer, user_agent = match.groups()
        method, url, _ = request.split()
        return {
            'ip': ip,
            'timestamp': datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S %z'),
            'method': method,
            'url': url,
            'status': int(status),
            'bytes_size': int(bytes_size),
            'referrer': referrer,
            'user_agent': user_agent
        }
    return None

def process_log_file(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            parsed = parse_log_line(line.strip())
            if parsed:
                logs.append(parsed)
    return pd.DataFrame(logs)

csv_file_path = 'C:\\Users\\syorg\\output.csv'  
df_geo = pd.read_csv(csv_file_path)
# Log dosyasını okuma
file_path = r"C:\Apache24\logs\access.log"
df_log = process_log_file(file_path)

df_combined = df_log.merge(df_geo, on='ip', how='left')
combined_csv_file_path = 'C:\\Users\\syorg\\combined_output.csv'  
df_combined.to_csv(combined_csv_file_path, index=False)
print(f"Birleşmiş veri '{combined_csv_file_path}' dosyasına kaydedildi.")


# Veri temizleme
df_log.dropna(inplace=True)  # Eksik verileri çıkar
df_log['url'] = df_log['url'].str.lower()  # URL'leri küçük harfe çevir
# df_combined DataFrame'ini kullanarak bilinmeyen ülkelere sahip satırları çıkarın
df_combined = df_combined[df_combined['country'] != 'Unknown']
# http://example.com olan satırları düşürmek için filtreleme
df_combined = df_combined[df_combined['referrer'] != 'http://example.com/blog/post-1 ']



combined_csv_file_path = 'C:\\Users\\syorg\\combined_output.csv'  
df_combined.to_csv(combined_csv_file_path, index=False)
print(f"Birleşmiş ve güncellenmiş veri '{combined_csv_file_path}' dosyasına kaydedildi.")

# Özellik çıkarımı
df_log = process_log_file(file_path)
df_log['hour'] = df_log['timestamp'].dt.hour
df_log['day'] = df_log['timestamp'].dt.day
df_log['is_weekend'] = df_log['timestamp'].dt.dayofweek.isin([5, 6])


# Ülkelere göre trafik analizi
country_traffic = df_combined['country'].value_counts()
print("Ülkelere Göre İstek Sayıları:\n", country_traffic)

# En popüler ülkeleri belirleme
top_countries = country_traffic.head(10)
print("En Popüler 10 Ülke:\n", top_countries)

# En çok istek yapan IP'ler ve ülkeleri
top_ips = df_combined.groupby('ip').agg({'country': 'first', 'url': 'count'}).sort_values('url', ascending=False).head(10)
print("\nEn Çok İstek Yapan IP'ler ve Ülkeleri:\n", top_ips)


# User-Agent analizi
df_log['device'] = df_log['user_agent'].apply(lambda ua: parse(ua).device.family)

# Oturum oluşturma
df_log['session'] = (df_log['ip'] != df_log['ip'].shift()).cumsum()

# Popüler sayfaları belirleme
popular_pages = df_log['url'].value_counts().head(10)

# HTTP durum kodları analizi
status_codes = df_log['status'].value_counts()

# Saatlik trafik analizi
hourly_traffic = df_log.groupby('hour').size()

# Ortalama yanıt boyutu
avg_response_size = df_log['bytes_size'].mean()

# En çok istek yapan IP'ler
top_ips = df_log['ip'].value_counts().head(10)

# Veri yapılandırma
structured_logs = df_log.to_dict('records')

# Sonuçları yazdırma
print("Popüler Sayfalar:")
print(popular_pages)
print("\nHTTP Durum Kodları:")
print(status_codes)
print("\nSaatlik Trafik:")
print(hourly_traffic)
print(f"\nOrtalama Yanıt Boyutu: {avg_response_size:.2f} bytes")
print("\nEn Çok İstek Yapan IP'ler:")
print(top_ips)


def vectorize_data(df):
    # IP adreslerini sayısal değerlere dönüştür
    df['ip_numeric'] = df['ip'].apply(lambda x: int(''.join([f"{int(part):03d}" for part in x.split('.')])))

    # Zaman damgasını sayısal değere dönüştür
    df['timestamp_numeric'] = df['timestamp'].astype('int64') // 10 ** 9

    # HTTP metodlarını one-hot encoding ile kodla
    method_dummies = pd.get_dummies(df['method'], prefix='method')

    # Path'leri TF-IDF ile vektörleştir
    tfidf = TfidfVectorizer(max_features=100)  # En yaygın 100 terimi kullan
    path_vectors = tfidf.fit_transform(df['url']).toarray()
    # Referrer'ı vektörleştir (basit bir yaklaşım)
    if 'referrer' in df.columns:
        df['referer_numeric'] = df['referrer'].apply(lambda x: hash(x) % 10 ** 8)  # 8 basamaklı bir sayıya dönüştür
    else:
        # Eğer 'referer' sütunu yoksa, varsayılan bir değer kullan
        df['referer_numeric'] = np.zeros(df.shape[0], dtype=np.int64) # 8 basamaklı bir sayıya dönüştür
    # HTTP Durum Kodlarını one-hot encoding ile vektörleştirme
    status_dummies = pd.get_dummies(df['status'], prefix='status')

    # Saatlik trafik verisini one-hot encoding ile vektörleştirme
    hour_dummies = pd.get_dummies(df['hour'], prefix='hour')

    # Ülke bilgisini one-hot encoding ile vektörleştirme
    if 'country' in df.columns:
        country_dummies = pd.get_dummies(df['country'], prefix='country')
    else:
        country_dummies = np.zeros((df.shape[0], 1))
    # User Agent'ı vektörleştir (basit bir yaklaşım)
    df['user_agent_numeric'] = df['user_agent'].apply(lambda x: hash(x) % 10 ** 8)

    # Sayısal özellikleri birleştir
    numeric_features = np.column_stack((
        df['ip_numeric'],
        df['timestamp_numeric'],
        df['status'],
        df['bytes_size'],
        df['referer_numeric'],
        df['user_agent_numeric'],
        method_dummies,
        path_vectors
    ))

    return numeric_features.astype('float32')


def create_faiss_index(vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    return index


def analyze_data(df):
    # En çok ziyaret edilen 10 sayfa
    top_pages = df['url'].value_counts().head(10)
    print("En çok ziyaret edilen 10 sayfa:\n", top_pages)

    # En çok kullanılan 5 HTTP metodu
    top_methods = df['method'].value_counts().head(5)
    print("\nEn çok kullanılan 5 HTTP metodu:\n", top_methods)

    # Zaman damgası analizi (istek sayısını saat dilimlerine göre gruplayın)
    df['hour'] = df['timestamp'].dt.hour
    hourly_requests = df['hour'].value_counts().sort_index()
    print("\nSaat dilimlerine göre istek sayıları:\n", hourly_requests)


def main():
    log_file_path = r"C:\Apache24\logs\access.log"
    

    # Log dosyasını işle
    df = process_log_file(log_file_path)
    print("Log dosyası işlendi. Veri şekli:", df.shape)

    # Verileri analiz et
    analyze_data(df)

    # Verileri vektörleştir
    vectors = vectorize_data(df)
    print("Veriler vektörleştirildi. Vektör şekli:", vectors.shape)

    # FAISS indeksi oluştur
    index = create_faiss_index(vectors)
    print("FAISS indeksi oluşturuldu. Indeks boyutu:", index.ntotal)

    # İndeksi kaydet (opsiyonel)
    faiss.write_index(index, "log_vectors.index")
    print("FAISS indeksi 'log_vectors.index' olarak kaydedildi.")


if __name__ == "__main__":
    main()