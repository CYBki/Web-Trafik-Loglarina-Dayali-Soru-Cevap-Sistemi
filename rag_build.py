import faiss
import numpy as np
import pandas as pd
import openai
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


# FAISS indeksini yükleyin
faiss_index = faiss.read_index("C:\\Apache24\\conf\\log_vectors.index")

# Verilerinizi yükleyin
df_combined = pd.read_csv('C:\\Users\\syorg\\combined_output.csv')

# Vektörleştiriciyi tanımlama ve eğitme
vectorizer = TfidfVectorizer(max_features=faiss_index.d)
path_vectors = vectorizer.fit_transform(df_combined['url']).toarray()

# Vektörleştiriciyi saklama
joblib.dump(vectorizer, 'vectorizer.joblib')

# Kaydedilen vektörleştiriciyi yükleme
vectorizer = joblib.load('vectorizer.joblib')

# OpenAI API Key
openai.api_key = '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'

# Sorgu vektörleştirme
def vectorize_query(query):
    query_vector = vectorizer.transform([query]).toarray().astype('float32')
    print(f"Sorgu vektörünün boyutu: {query_vector.shape}")
    return query_vector

# Log kayıtlarını getir
def retrieve_logs(query, faiss_index, df):
    query_vector = vectorize_query(query)
    assert query_vector.shape[1] == faiss_index.d, \
        f"Sorgu vektörünün boyutu ({query_vector.shape[1]}) ile FAISS indeksinin boyutu ({faiss_index.d}) eşleşmiyor."
    _, indices = faiss_index.search(query_vector, k=5)  # En yakın 5 logu getir
    print(f"En yakın vektörlerin indeksleri: {indices[0]}")
    
    if len(indices[0]) > 0:
        retrieved_logs = df.iloc[indices[0]]
        print(f"Bulunan log kayıtları: \n{retrieved_logs}")
    else:
        print("En yakın vektörler bulunamadı.")
        retrieved_logs = pd.DataFrame()  # Boş bir DataFrame döndür
    
    return retrieved_logs

# IP adresine göre filtreleme
def filter_logs_by_ip(ip_address, df):
    filtered_logs = df[df['ip'] == ip_address]
    return filtered_logs

# Yanıt oluşturma
def generate_response(retrieved_logs, query):
    if retrieved_logs.empty:
        return "Sorguya uygun log bulunamadı."
    
    context = "\n".join([f"Log girişi: {row}" for _, row in retrieved_logs.iterrows()])
    messages = [
        {"role": "system", "content": "Sen bir yardımcısın."},
        {"role": "user", "content": f"Kullanıcı sorgusu: {query}\n\nİlgili loglar:\n{context}\n\nKullanıcının sorgusuna yukarıdaki loglara dayanarak bir yanıt oluşturun."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Sorguya yanıt oluştur
def answer_query(query, ip_address, faiss_index, df):
    # IP adresine göre filtreleme
    filtered_logs = filter_logs_by_ip(ip_address, df)
    
    if filtered_logs.empty:
        return f"{ip_address} IP adresine ait log bulunamadı."

    # Filtrelenmiş loglardan bir sorgu oluşturma
    logs_text = " ".join(filtered_logs['url'])
    response_from_filtered_logs = generate_response(filtered_logs, query)

    # Sorguyu FAISS indeksi üzerinde kullanma
    response_from_faiss = retrieve_logs(logs_text, faiss_index, df)
    
    # Sonuçları birleştirip döndürme
    combined_response = f"Filtrelenmiş loglara dayalı yanıt:\n{response_from_filtered_logs}\n\nFAISS'e dayalı yanıt:\n{response_from_faiss}"
    return combined_response

# Sık kullanılan URL'leri analiz etme
def analyze_frequent_urls(ip_address, df):
    filtered_logs = filter_logs_by_ip(ip_address, df)
    if filtered_logs.empty:
        return f"{ip_address} IP adresine ait log bulunamadı."

    # URL'leri gruplandır ve say
    url_counts = filtered_logs['url'].value_counts()
    return url_counts


# Kodun çalıştırılması
if __name__ == "__main__":
    query = "Bu IP kaç kere istek göndermiştir?"
    ip_address = "215.135.113.15"
    response = answer_query(query, ip_address, faiss_index, df_combined)
    print(response)

