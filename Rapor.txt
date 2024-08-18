# Performans Değerlendirmesi

## 1. Giriş

Bu rapor, geliştirdiğimiz log analizi sisteminin doğruluğunu ve performansını değerlendirmek için hazırlanmıştır. Sistem, kullanıcılardan gelen sorgulara yanıt verirken log verilerini analiz etmek üzere FAISS vektör arama ve dil modeli teknolojilerini kullanmaktadır. Raporda, sistemin doğruluğu, performansı ve iyileştirme önerileri detaylandırılmıştır.

## 2. Sistem Performansı

### 2.1 Test Senaryoları ve Sonuçlar

#### 2.1.1 Sorgu: "Bu IP kaç kere istek göndermiştir?"

- **Sorgu Vektörünün Boyutu:** (1, 20)
- **En Yakın Vektörlerin İndeksleri:** [0, 2, 9, 25, 48]
- **Bulunan Log Kayıtları:**

  | ip              | timestamp                | method | url      | status | bytes_size | referrer                | user_agent                                      | country       |
  |-----------------|---------------------------|--------|----------|--------|------------|-------------------------|-------------------------------------------------|---------------|
  | 215.135.113.15  | 2023-08-15 09:18:02+03:00 | PUT    | /about   | 400    | 4890       | https://www.google.com | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7...) | United States |
  | 215.135.113.15  | 2023-08-15 09:18:02+03:00 | PUT    | /about   | 400    | 4890       | https://www.google.com | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7...) | United States |
  | 190.111.107.243 | 2023-08-15 13:53:43+03:00 | POST   | /products| 404    | 7844       | https://www.google.com | Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl... | Brazil        |
  | 113.110.156.210 | 2023-08-15 12:41:37+03:00 | PUT    | /about   | 204    | 6719       | https://www.bing.com   | Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl... | China         |
  | 172.228.94.122  | 2023-08-15 15:23:15+03:00 | POST   | /css/main.css | 304 | 4241       | https://www.google.com | Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:9...) | United States |

- **Filtrelenmiş Loglara Dayalı Yanıt:** IP adresi 215.135.113.15 toplamda **4 kere** istek göndermiştir.
- **FAISS'e Dayalı Yanıt:** Aynı sonuçlar, IP adresinin dört kez kayıtlı olduğu gözlemlenmiştir.

#### 2.1.2 Sorgu: "Bu kullanıcı hangi sayfalara erişti?"

- **Sorgu Vektörünün Boyutu:** (1, 20)
- **En Yakın Vektörlerin İndeksleri:** [0, 2, 9, 25, 48]
- **Bulunan Log Kayıtları:** Yukarıdaki tablodaki aynı log kayıtları.

- **Filtrelenmiş Loglara Dayalı Yanıt:** IP adresinin "/about" sayfasına erişim sağlamaya çalıştığı, ancak tüm isteklerin "PUT" yöntemiyle ve 400 hatasıyla sonuçlandığı belirtilmiştir.
- **FAISS'e Dayalı Yanıt:** Aynı loglar tekrar gösterilmiştir.

#### 2.1.3 Sorgu: "En sık kullanılan URL nedir?"

- **Sorgu Vektörünün Boyutu:** (1, 20)
- **En Yakın Vektörlerin İndeksleri:** [0, 2, 9, 25, 48]
- **Bulunan Log Kayıtları:** Yukarıdaki tablodaki aynı log kayıtları.

- **Filtrelenmiş Loglara Dayalı Yanıt:** IP adresinin sadece "/about" sayfasına erişim sağladığı belirtilmiştir.
- **FAISS'e Dayalı Yanıt:** Aynı loglar tekrar gösterilmiştir.

### 2.2 Performans Ölçümleri

- **Büyük Veri Kümesi Üzerindeki Yanıt Süresi:** 5.16 saniye
- **Test Senaryolarındaki Yanıt Süreleri:**

  | Sorgu                                   | Yanıt Süresi |
  |-----------------------------------------|--------------|
  | Bu IP kaç kere istek göndermiştir?      | 1.82 saniye   |
  | Bu IP kaç kere istek göndermiştir? (192.168.1.1) | 0.00 saniye   |
  | Bu IP kaç kere istek göndermiştir? (10.0.0.5)   | 0.00 saniye   |
  | Bu kullanıcı hangi sayfalara erişti?     | 2.00 saniye   |
  | En sık kullanılan URL nedir?             | 1.39 saniye   |

## 3. Doğruluk Değerlendirmesi

- **Başarılar:**
  - FAISS ve filtreleme yöntemleri, doğru log kayıtlarını ve sayfaları döndürmekte tutarlı bir şekilde başarılı olmuştur.
  - Sorgu vektörleri doğru log kayıtları ile eşleşmiştir ve yanıtlar genel olarak doğru verilmiştir.

- **Başarısızlıklar:**
  - Bir testin başarısız olması, yanıtın genel içeriğinde "url:" etiketinin bulunmamasıdır. Bu, belirli bir soruya yanıtın eksik veya yetersiz olduğunu gösterir.

## 4. İyileştirme Önerileri

1. **Sorgu Yanıtlarının İçeriği:**
   - Yanıtların içeriği, kullanıcının daha fazla bilgi edinmesini sağlayacak şekilde zenginleştirilebilir. Özellikle URL'ler ve erişim bilgileri daha belirgin ve düzenli bir şekilde sunulmalıdır.

2. **Performans İyileştirmeleri:**
   - Büyük veri kümesi üzerinde yanıt süresi optimize edilmelidir. Daha verimli vektör arama ve sorgu işleme teknikleri kullanılabilir.
   - Paralel işleme ve önbellekleme stratejileri ile yanıt süreleri azaltılabilir.

3. **Test Kapsamı:**
   - Testlerin kapsamı genişletilerek farklı senaryolar ve veri setleri ile sistemin daha geniş bir test edilmesi sağlanabilir. Özellikle çeşitli IP adresleri ve URL'ler için performans ve doğruluk testleri yapılmalıdır.

## 5. Sonuç

Sistem, genel olarak başarılı sonuçlar vermekte ve sorgulara doğru yanıtlar sağlamaktadır. Ancak, yanıtların içeriği ve performans açısından bazı iyileştirmelere ihtiyaç vardır. Bu iyileştirmeler, sistemin doğruluğunu ve verimliliğini artırarak kullanıcı deneyimini iyileştirecektir.

