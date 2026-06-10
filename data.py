import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

DOSYA_YOLU = "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"
VEKTOR_DB_KLASORU = "vektor_veritabani"
MODEL_KLASORU = MODEL_KLASORU = r"C:\Users\E\PycharmProjects\PythonProject\models--sentence-transformers--all-MiniLM-L6-v2"

print("1. Adım: Veri setinden örnek satırlar okunuyor...")
df = pd.read_csv(DOSYA_YOLU, skiprows=range(1, 250000), nrows=500)
df.columns = df.columns.str.strip()

print("2. Adım: Log satırları metne dönüştürülüyor...")
log_belgeleri = []
for indeks, satir in df.iterrows():
    log_metni = (
        f"Zaman: {satir.get('Timestamp', 'Bilinmiyor')} - "
        f"Kaynak IP: {satir.get('Source IP', 'Bilinmiyor')} -> "
        f"Hedef IP: {satir.get('Destination IP', 'Bilinmiyor')} - "
        f"Hedef Port: {satir.get('Destination Port', 'Bilinmiyor')} - "
        f"Protokol: {satir.get('Protocol', 'Bilinmiyor')} - "
        f"Etiket/Durum: {satir.get('Label', 'Bilinmiyor')}"
    )
    doc = Document(page_content=log_metni, metadata={"satir_no": indeks})
    log_belgeleri.append(doc)

print("3. Adım: Embedding modeli yükleniyor...")
embedding_modeli = HuggingFaceEmbeddings(
    model_name=r"C:\Users\E\PycharmProjects\PythonProject\models--sentence-transformers--all-MiniLM-L6-v2\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
)

print("4. Adım: Vektörler hesaplanıyor ve ChromaDB'ye kaydediliyor...")
vektor_db = Chroma.from_documents(
    documents=log_belgeleri,
    embedding=embedding_modeli,
    persist_directory=VEKTOR_DB_KLASORU
)

print(f"\nBaşarılı! {len(log_belgeleri)} adet log vektörleştirildi ve '{VEKTOR_DB_KLASORU}' klasörüne kaydedildi.")