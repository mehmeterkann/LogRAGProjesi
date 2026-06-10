from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

VEKTOR_DB_KLASORU = "vektor_veritabani"
MODEL_KLASORU = r"C:\Users\E\PycharmProjects\PythonProject"

print("1. Adım: Sistem yükleniyor...")

embedding_modeli = HuggingFaceEmbeddings(
    model_name=r"C:\Users\E\PycharmProjects\PythonProject\models--sentence-transformers--all-MiniLM-L6-v2\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
)
vektor_db = Chroma(
    persist_directory=VEKTOR_DB_KLASORU,
    embedding_function=embedding_modeli
)

try:
    llm = OllamaLLM(model="llama3.2", temperature=0.1, num_ctx=2048)
except Exception as e:
    print(f"\nHata: Ollama çalışmıyor olabilir! ({e})")
    exit()

print("Sistem hazır! Sorgu bekleniyor...")
print("-" * 50)

soru = "Sistemde herhangi bir şüpheli aktivite veya Port Taraması (PortScan) var mı? Varsa detayları raporla."
print(f"\nSorulan Soru: {soru}\n")
print("Yapay zeka log klasöründe arama yapıyor...")

benzer_loglar = vektor_db.similarity_search(soru, k=5)

log_icerikleri = ""
for i, doc in enumerate(benzer_loglar, 1):
    log_icerikleri += f"\n[Log {i}]: {doc.page_content}"

istek_metni = f"""
Sen bir siber güvenlik uzmanı yapay zeka ajanısın.
Aşağıda sistem loglarından filtrelenmiş 5 adet kritik ağ trafiği kaydı bulunmaktadır.
Bu logları incele ve kullanıcının sorusuna kanıta dayalı, Türkçe ve teknik bir özet rapor sun.

Kullanıcının Sorusu: {soru}

Sistemden Gelen Kritik Loglar:
{log_icerikleri}

Analiz Raporun (Türkçe yaz):
"""

cevap = llm.invoke(istek_metni)

print("\n" + "=" * 20 + " YAPAY ZEKA ANALİZ RAPORU " + "=" * 20)
print(cevap)
print("=" * 66)