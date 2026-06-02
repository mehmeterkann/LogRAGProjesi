from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

print("1. Adım: Lokal sistem yükleniyor, lütfen bekleyin...")

veri_tabani_klasoru = "vektor_veritabani"
embedding_modeli = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vektor_db = Chroma(
    persist_directory=veri_tabani_klasoru,
    embedding_function=embedding_modeli
)

try:
    yapay_zekacik = OllamaLLM(
        model="llama3.2",
        temperature=0.1,  # Daha net ve kararlı cevaplar vermesi için
        num_ctx=2048      # Hafıza boyutunu küçülttük ki RAM'e rahat sığsın
    )
except Exception as e:
    print("\nHata: Ollama sistemi arka planda çalışmıyor olabilir!")
    exit()

print("Sistem hazır! Güvenlik analisti sorgusu bekleniyor...")
print("-" * 50)

soru = "Sistemde herhangi bir şüpheli aktivite veya Port Taraması (PortScan) var mı? Varsa detayları raporla."

print(f"\nSorulan Soru: {soru}\n")
print("Yapay zeka log klasöründe arama yapıyor ve cevabı hazırlıyor...")

benzer_loglar = vektor_db.similarity_search(soru, k=5)

log_icerikleri = ""
for i, doc in enumerate(benzer_loglar, 1):
    log_icerikleri += f"\n[Log {i}]: {doc.page_content}"

istek_metni = f"""
Sen bir siber güvenlik uzmanı yapay zeka ajanısın. 
Aşağıda, sistem loglarından senin için filtrelenmiş 5 adet kritik ağ trafiği kaydı bulunmaktadır.
Bu logları incele ve kullanıcının sorusuna kanıta dayalı, Türkçe ve teknik bir özet rapor sun.

Kullanıcının Sorusu: {soru}

Sistemden Gelen Kritik Loglar:
{log_icerikleri}

Analiz Raporun (Lütfen anlaşılır ve Türkçe yaz):
"""

cevap = yapay_zekacik.invoke(istek_metni)

print("\n" + "="*20 + " YAPAY ZEKA ANALİZ RAPORU " + "="*20)
print(cevap)
print("="*66)