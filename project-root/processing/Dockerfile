FROM bitnami/spark:latest

USER root

# Install Python and pip packages
RUN apt-get update && apt-get install -y python3 python3-pip openjdk-11-jdk && \
    pip3 install pyspark mysql-connector-python

WORKDIR /app

COPY process_batch.py .

CMD ["python3", "process_batch.py"]
