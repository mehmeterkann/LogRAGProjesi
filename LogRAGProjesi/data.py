import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
import os


dosya_yolu = "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv"

print("1. Adım: Veri setinden örnek satırlar okunuyor...")

df = pd.read_csv(dosya_yolu, skiprows=range(1, 50000), nrows=500)
df.columns = df.columns.str.strip()

log_belgeleri = []
print("2. Adım: Log satırları metne dönüştürülüyor...")

for indeks, satir in df.iterrows():
    log_metni = (
        f"Zaman: {satir.get('Timestamp', 'Bilinmiyor')} - "
        f"Kaynak IP: {satir.get('Source IP', 'Bilinmiyor')} -> Hedef IP: {satir.get('Destination IP', 'Bilinmiyor')} - "
        f"Hedef Port: {satir.get('Destination Port', 'Bilinmiyor')} - "
        f"Protokol: {satir.get('Protocol', 'Bilinmiyor')} - "
        f"Etiket/Durum: {satir.get('Label', 'Bilinmiyor')}"
    )

    meta_veri = {"satir_no": indeks}
    doc = Document(page_content=log_metni, metadata=meta_veri)
    log_belgeleri.append(doc)

print("3. Adım: Embedding modeli yükleniyor (İnternet hızına göre biraz sürebilir)...")
embedding_modeli = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("4. Adım: Vektörler hesaplanıyor ve ChromaDB'ye kaydediliyor...")
veri_tabani_klasoru = "vektor_veritabani"

vektor_db = Chroma.from_documents(
    documents=log_belgeleri,
    embedding=embedding_modeli,
    persist_directory=veri_tabani_klasoru
)

print(f"\nBaşarılı! {len(log_belgeleri)} adet log vektörleştirildi ve '{veri_tabani_klasoru}' klasörüne kaydedildi.")