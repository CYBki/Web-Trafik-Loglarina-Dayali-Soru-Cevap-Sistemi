# Web Trafik Loglarına Dayalı Soru-Cevap Sistemi

Bu proje, bir web sitesinin trafik loglarını kullanarak doğal dildeki sorulara yanıt verebilen bir Soru-Cevap (Q&A) sistemi geliştirmeyi amaçlamaktadır. Proje, Retrieval-Augmented Generation (RAG) modeli temelinde çalışmakta olup, log verilerini analiz ederek en uygun yanıtları oluşturur.

## İçindekiler
- [Proje Hakkında](#proje-hakkında)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Kurulum](#kurulum)
  - [Gereksinimler](#gereksinimler)
  - [Depoyu Klonlama](#depoyu-klonlama)
## Proje Hakkında
Bu proje, web trafik logları kullanılarak bir soru-cevap sistemi geliştirmeyi hedefler. Sistem, kullanıcı sorularını alır, ilgili log verilerini bulur ve bu verilere dayanarak bir yanıt oluşturur. Projenin temel amacı, büyük log dosyaları üzerinde etkili bir şekilde çalışabilen ve anlamlı yanıtlar üretebilen bir sistem geliştirmektir.

### Proje Adımları
1. **Veri Hazırlığı ve Ön İşleme**:
   - Log dosyasındaki verilerin analiz edilmesi, temizlenmesi ve yapılandırılması.
   - Verilerin vektörlere dönüştürülmesi ve vektör veri tabanına yüklenmesi.

2. **RAG Modelinin Kurulumu**:
   - Bilgi Alma: Vektör veri tabanını kullanarak en uygun log kayıtlarının bulunması.
   - Jeneratif Model: Bulunan log kayıtlarıyla yanıt oluşturmak için bir dil modeli kullanılması(gpt).

3. **Sistem Entegrasyonu ve Test**:
   - Bilgi alma ve jeneratif modelin entegre edilmesi.
   - Kullanıcıdan gelen bir soruya yanıt verebilen bir sistem tasarlanması.

4. **Performans Değerlendirmesi**:
   - Sistemin doğruluğu ve performansının değerlendirilmesi.
   - Yanıt kalitesini artırmak için önerilerde bulunulması.

## Kullanılan Teknolojiler
- **Python**: Projenin geliştirilmesi için kullanılan ana programlama dili. Python 3.8 sürümü kullanılması tavsiye edilir. FAISS python ile 3.8 sürümüne kadar uyumlu çalışabilmektedir.
- **FAISS**: Log verilerini vektörlere dönüştürmek ve bu vektörler üzerinde hızlı arama yapmak için kullanılan kütüphane.
- **OpenAI GPT**: Kullanıcı sorularına yanıt oluşturmak için kullanılan jeneratif dil modeli.
- **Unittest**: Projedeki bileşenlerin test edilmesi için kullanılan Python test kütüphanesi.

## Kurulum

### Gereksinimler
- Python 3.8
- Git
- Sanal ortam (virtualenv veya conda)

### Depoyu Klonlama
Projeyi çalıştırmak için aşağıdaki adımları izleyin:

```bash
git clone https://github.com/CYBki/Web-Trafik-Loglarina-Dayali-Soru-Cevap-Sistemi.git
cd project-repo
