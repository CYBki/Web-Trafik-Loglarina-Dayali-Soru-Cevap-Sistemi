import unittest
import faiss
import pandas as pd
import time
from rag_build import vectorize_query, filter_logs_by_ip, answer_query, generate_response  # Ana modüldeki fonksiyonlar
from rag_build import faiss_index, df_combined  # FAISS index ve veri dosyasını import edin

class TestLogSystem(unittest.TestCase):
    def test_vectorize_query(self):
        query = "örnek sorgu"
        result = vectorize_query(query)
        self.assertEqual(result.shape[1], faiss_index.d)  # FAISS indeks boyutu ile eşleşmeli

    def test_filter_logs_by_ip(self):
        ip_address = "215.135.113.15"
        result = filter_logs_by_ip(ip_address, df_combined)
        self.assertFalse(result.empty)  # Bilinen bir IP için sonucun boş olmadığından emin olun

    def test_answer_query(self):
        query = "Bu IP'nin eriştiği sayfalar nelerdir?"
        ip_address = "215.135.113.15"
        response = answer_query(query, ip_address, faiss_index, df_combined)
        self.assertIn("Filtrelenmiş loglara dayalı yanıt", response)
        self.assertIn("FAISS'e dayalı yanıt", response)

def extended_performance_test(query, ip_address):
    start_time = time.time()
    response = answer_query(query, ip_address, faiss_index, df_combined)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Sorgu: {query}, IP: {ip_address}, Yanıt süresi: {duration:.2f} saniye")
    return duration

# Farklı sorgular ve IP adresleri ile test etme
queries = ["Bu IP kaç kere istek göndermiştir?", "Bu kullanıcı hangi sayfalara erişti?", "En sık kullanılan URL nedir?"]
ip_addresses = ["215.135.113.15", "192.168.1.1", "10.0.0.5"]

for query in queries:
    for ip in ip_addresses:
        extended_performance_test(query, ip)

from memory_profiler import profile

@profile
def memory_test():
    query = "Bu IP kaç kere istek göndermiştir?"
    ip_address = "215.135.113.15"
    response = answer_query(query, ip_address, faiss_index, df_combined)
    print(response)

# Bellek testi
memory_test()

class ExtendedTestLogSystem(unittest.TestCase):
   def test_generate_response(self):
        ip_address = "215.135.113.15"
        filtered_logs = filter_logs_by_ip(ip_address, df_combined)
        query = "Bu kullanıcı hangi sayfalara erişti?"
        response = generate_response(filtered_logs, query)
        self.assertIn("URL:", response)  # Yanıtın genel içeriğinde URL'lerin olduğuna emin olun
        self.assertIn("/about", response)  # Belirli URL'lerin yanıt içinde olduğuna emin olun
        self.assertNotIn("sayfalara erişti", response)  # "sayfalara erişti" ifadesinin testteki önemli olmadığını kontrol edin





def scalability_test(df_large):
    query = "Bu kullanıcı hangi sayfalara erişti?"
    ip_address = "215.135.113.15"
    
    start_time = time.time()
    response = answer_query(query, ip_address, faiss_index, df_large)
    end_time = time.time()
    
    print(f"Büyük veri kümesi üzerinde yanıt süresi: {end_time - start_time:.2f} saniye")
    return response

# Büyük bir veri kümesi ile test edin
df_large = pd.concat([df_combined] * 100)  # Veri setini 100 kat büyütme
scalability_test(df_large)

if __name__ == "__main__":
    unittest.main()
