FROM python:3.9

WORKDIR /app

COPY app.py .

RUN pip install streamlit mysql-connector-python pandas

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
