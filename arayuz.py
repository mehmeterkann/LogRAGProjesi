import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

st.set_page_config(page_title="LogRAG Analiz Paneli", layout="wide")

st.title("Siber Güvenlik Log Analiz Paneli (RAG)")
st.markdown("---")

st.sidebar.header("Sistem Bilgileri")
st.sidebar.info("Model: Llama 3.2 (Lokal)\nVeri Seti: PortScan Logs")
st.sidebar.write(
    "Bu sistem, log dosyalarınızı analiz ederek "
    "yapay zeka destekli güvenlik raporları üretir."
)

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
VEKTOR_DB_KLASORU = "vektor_veritabani"
# Docker içinde /app/model, lokalde mevcut yol
MODEL_YOLU = os.environ.get("MODEL_PATH", "/app/model")


@st.cache_resource
def sistemi_yukle():
    embedding_modeli = HuggingFaceEmbeddings(model_name=MODEL_YOLU)
    vektor_db = Chroma(
        persist_directory=VEKTOR_DB_KLASORU,
        embedding_function=embedding_modeli
    )
    llm = OllamaLLM(
        model="llama3.2",
        base_url=OLLAMA_HOST,
        temperature=0.1,
        num_ctx=2048
    )
    return vektor_db, llm


vektor_db, llm = sistemi_yukle()

soru = st.text_input(
    "Sorgulamak istediğiniz güvenlik durumunu yazın:",
    "Sistemde Port Taraması (PortScan) belirtileri var mı?"
)

if st.button("🔍 Analiz Et"):
    with st.spinner("Yapay zeka logları inceliyor..."):
        benzer_loglar = vektor_db.similarity_search(soru, k=5)

        with st.expander("📋 İncelenen Ham Log Kayıtları"):
            for doc in benzer_loglar:
                st.code(doc.page_content)

        log_icerikleri = "\n".join([doc.page_content for doc in benzer_loglar])
        prompt = (
            "Sen bir güvenlik uzmanısın. "
            "Aşağıdaki loglara bakarak soruyu Türkçe cevapla:\n\n"
            f"Loglar:\n{log_icerikleri}\n\n"
            f"Soru: {soru}"
        )

        cevap = llm.invoke(prompt)

        st.subheader("🤖 Yapay Zeka Analiz Raporu")
        st.success(cevap)

st.markdown("---")
st.caption("LogRAG Projesi — 2024")