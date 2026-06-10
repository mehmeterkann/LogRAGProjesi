FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements_cpu.txt .
RUN pip install --no-cache-dir -r requirements_cpu.txt

COPY arayuz.py .
COPY data.py .
COPY sorgu_sistemi.py .

COPY vektor_veritabani/ ./vektor_veritabani/
COPY model/ ./model/

RUN mkdir -p /root/.streamlit
RUN echo '\
[server]\n\
headless = true\n\
port = 8501\n\
address = "0.0.0.0"\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
' > /root/.streamlit/config.toml

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "arayuz.py", "--server.port=8501", "--server.address=0.0.0.0"]
