import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

st.set_page_config(page_title="LogRAG Analiz Paneli", layout="wide")

st.title("Siber Güvenlik Log Analiz Paneli (RAG)")
st.markdown("---")

st.sidebar.header("Sistem Bilgileri")
st.sidebar.info("Model: Llama 3.2 (Lokal)\nVeri Seti: PortScan Logs")
st.sidebar.write("Bu sistem, log dosyalarınızı analiz ederek yapay zeka destekli güvenlik raporları üretir.")


@st.cache_resource
def sistemi_yukle():
    embedding_modeli = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vektor_db = Chroma(persist_directory="vektor_veritabani", embedding_function=embedding_modeli)
    llm = OllamaLLM(model="llama3.2", temperature=0.1, num_ctx=2048)
    return vektor_db, llm


vektor_db, llm = sistemi_yukle()

soru = st.text_input("Sorgulamak istediğiniz güvenlik durumunu yazın:",
                     "Sistemde Port Taraması (PortScan) belirtileri var mı?")

if st.button("Analiz Et"):
    with st.spinner("Yapay zeka logları inceliyor..."):
        benzer_loglar = vektor_db.similarity_search(soru, k=5)

        with st.expander("İncelenen Ham Log Kayıtları"):
            for doc in benzer_loglar:
                st.code(doc.page_content)

        log_icerikleri = "\n".join([doc.page_content for doc in benzer_loglar])
        prompt = f"Sen bir güvenlik uzmanısın. Aşağıdaki loglara bakarak soruyu Türkçe cevapla:\n\nLoglar:\n{log_icerikleri}\n\nSoru: {soru}"

        cevap = llm.invoke(prompt)

        st.subheader("Yapay Zeka Analiz Raporu")
        st.success(cevap)

st.markdown("---")
st.caption("LogRAG Projesi - 2024")