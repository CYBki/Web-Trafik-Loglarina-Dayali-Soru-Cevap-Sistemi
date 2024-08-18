# Performans Değerlendirmesi

## İçindekiler

1. [Giriş](#1-giriş)
2. [Sistem Performansı](#2-sistem-performansı)
   - [Test Senaryoları ve Sonuçlar](#21-test-senaryoları-ve-sonuçlar)
   - [Performans Ölçümleri](#22-performans-ölçümleri)
3. [Doğruluk Değerlendirmesi](#3-doğruluk-değerlendirmesi)
4. [İyileştirme Önerileri](#4-iyileştirme-önerileri)
5. [Sorun Çözümü Raporu](#5-sorun-çözümü-raporu)
6. [Genel Öneriler](#6-genel-öneriler)
7. [Sonuç](#7-sonuç)

## 1. Giriş

Bu rapor, geliştirdiğimiz log analizi sisteminin doğruluğunu ve performansını değerlendirmek için hazırlanmıştır. Sistem, kullanıcılardan gelen sorgulara yanıt verirken log verilerini analiz etmek üzere FAISS vektör arama ve dil modeli teknolojilerini kullanmaktadır. Raporda, sistemin doğruluğu, performansı ve iyileştirme önerileri detaylandırılmıştır.

## 2. Sistem Performansı

### 2.1 Test Senaryoları ve Sonuçlar

#### 2.1.1 Sorgu: "Bu IP kaç kere istek göndermiştir?"

- **Sorgu Vektörünün Boyutu:** (1, 20)
- **En Yakın Vektörlerin İndeksleri:** [0, 2, 9, 25, 48]
- **Bulunan Log Kayıtları:**

  | ip              | timestamp                | method | url      | status | bytes_size | referrer                | user_agent                                      | country       |
  |-----------------|--------------------------|--------|----------|--------|------------|-------------------------|-------------------------------------------------|---------------|
  | 215.135.113.15  | 2023-08-15 09:18:02+03:00 | PUT    | /about   | 400    | 4890       | https://www.google.com | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7...) | United States |
  | 215.135.113.15  | 2023-08-15 09:18:02+03:00 | PUT    | /about   | 400    | 4890       | https://www.google.com | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7...) | United States |
  | 190.111.107.243 | 2023-08-15 13:53:43+03:00 | POST   | /products| 404    | 7844       | https://www.google.com | Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl... | Brazil        |
  | 113.110.156.210 | 2023-08-15 12:41:37+03:00 | PUT    | /about   | 204    | 6719       | https://www.bing.com   | Mozilla/5.0 (Windows NT 10.0; Win64; x64) Appl... | China         |
  | 172.228.94.122  | 2023-08-15 15:23:15+03:00 | POST   | /css/main.css | 304 | 4241       | https://www.google.com | Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:9...) | United States |

- **Filtrelenmiş Loglara Dayalı Yanıt:**
Verilen loglara göre, IP adresi **215.135.113.15** toplamda **4 kez** istek göndermiştir. Tüm istekler **PUT** metodu ile **/about** URL'sine yapılmış ve tüm isteklere **400** durum kodu ile yanıt verilmiştir.
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
  | Bu IP kaç kere istek göndermiştir?      | 1.82 saniye  |
  | Bu IP kaç kere istek göndermiştir? (192.168.1.1) | 0.00 saniye  |
  | Bu IP kaç kere istek göndermiştir? (10.0.0.5)   | 0.00 saniye  |
  | Bu kullanıcı hangi sayfalara erişti?     | 2.00 saniye  |
  | En sık kullanılan URL nedir?             | 1.39 saniye  |

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

## 5. Sorun Çözümü Raporu

### Sunucu Başlatma Sorunları

**Hata Mesajları ve Çözümler**

1. **Hata:** httpd.exe: Syntax error on line 75  
   **Açıklama:** httpd.conf dosyasının 75. satırında bulunan mod_actions.so modülü yüklenemedi.  
   **Çözüm:** httpd.conf dosyasının 75. satırını yorum satırına alarak bu hatayı geçici olarak çözdüm. Ancak diğer satırlarda aynı hata ile karşılaşmaya başladım.

2. **Hata:** AH00558: httpd.exe: Could not reliably determine the server's fully qualified domain name  
   **Açıklama:** Sunucu, tam nitelikli etki alanı adını belirleyemediği için bu hata mesajını verdi.  
   **Çözüm:** httpd.conf dosyasındaki ServerName direktifini yorum satırından çıkardım ve uygun bir değer atayarak sunucuyu yeniden başlattım.  
   Sonuç olarak, httpd.exe -k status komutunu kullanarak sunucunun çalıştığını doğruladım ve "It works!" mesajını aldım.

### Log Verisi Yönetimi

Log dosyalarını manuel olarak oluşturdum ve daha fazla çeşitlilik sağlamak amacıyla bir Python scripti kullanarak logları 1100 civarında artırdım. Verileri analiz ettim ve ayıkladım. GeoIP2 veritabanını kullanarak IP adreslerinden ülke bilgisi çıkarımı yaparak değerli içgörüler elde ettim.

### Vektör Veritabanı Yönetimi

Vektörlere dönüştürme işlemi için FAISS kullanmayı tercih ettim. FAISS'in yerel olarak çalıştırılabilir olması ve kurulumunun daha kolay olması nedeniyle bu aracı seçtim. FAISS'i import ederken çeşitli sorunlarla karşılaştım ve gpt/Stack Overflow gibi sitelerde çözümü bulamayınca FAISS in dokümanına gidip incelemeye başlayınca  python'ın 3.8 versiyonuna kadar desteklediğini farkettim ve bu sorunları çözdüm.

### RAG (Retrieval-Augmented Generation) Kurulum Sorunları

Kullanıcının belirttiği IP adresi için sonuç bulunamadı hataları aldım. Daha fazla log kaydı gerektiğini belirten mesajlar aldım. Önceki aşamalarda temizlenmiş verilerin doğru bir şekilde işlenmediğini fark ettim bir kaç aşama öncesine gittim ve verileri doğru şekilde kaydedip işleyerek sorunu çözdüm.

## 6. Genel Öneriler

- **Streaming Data Kullanımı:** Performansı artırmak için gerçek zamanlı veri akışlarını değerlendirebilir. Bu, sistemin yanıt süresini ve genel performansını iyileştirebilir.
- **Özellik çıkarımı:**
- IP den ülke çıkarımı yaptığım gibi sonucu etkileyecek bir çok özellik vardır bunların araştırılması (gerekirse kendi kendimize deneyerek bulduğumuz sistemi etkileyen özellikler) ve özellik çıkarımı uygulamak sistemin performansını artıracaktır.
- Sistemin cevaplarının kalitesinde en büyük rol oynayan doğal dil modelleridir. Dil modeli ne kadar güçlü olursa, cevapların kalitesi de o kadar yüksek olur.
- Bu da demek oluyor ki
- Veri Miktarı ve Çeşitliliği: Dil modeli, geniş ve çeşitli veri kümeleriyle eğitildikçe, farklı konularda daha iyi yanıtlar üretebilir.

Modelin Mimarisi: Modelin karmaşıklığı ve derinliği, ne kadar bilgiyi işleyebileceğini ve ne kadar doğru yanıtlar verebileceğini etkiler.

Bağlamsal Anlayış: Modelin, kullanıcının sorgusunu ve bağlamını doğru bir şekilde anlaması, kaliteli cevaplar üretmek için kritiktir.

Güncellenme Sıklığı: Modelin ne kadar güncel olduğu, özellikle hızlı değişen bilgileri doğru bir şekilde sunabilmesi açısından önemlidir.

İnferans Hızı: Cevapların oluşturulma süresi, kullanıcı deneyimini etkileyen bir diğer faktördür.
bu kriterler göz önüne alınarak seçilen llm ler daha iyi cevaplar almada büyük bir etken(claude/gpt/gemini).

## 7. Sonuç

Sistem, genel olarak başarılı sonuçlar vermekte ve sorgulara doğru yanıtlar sağlamaktadır. Ancak, yanıtların içeriği ve performans açısından bazı iyileştirmelere ihtiyaç vardır. Bu iyileştirmeler, sistemin doğruluğunu ve verimliliğini artırarak kullanıcı deneyimini iyileştirecektir.
