# Batch Processing System for Service Recommendations

## Overview

This project implements a modular, containerized batch-processing data architecture to ingest, clean, and aggregate establishment data across various U.S. states. The system supports a machine learning application and a dashboard that recommends establishments based on service types (e.g., delivery, plumbing, air conditioning) and location, using insights from customer ratings and reviews.

The architecture uses:
- Docker Compose to orchestrate services (ingestion, processing, storage, dashboard)
- PySpark to perform daily aggregation and preprocessing
- MySQL (Dockerized) to store processed data
- Streamlit to display insights interactively

## Components

- `docker-compose.yml`  
  Orchestrates four services:  
  - `mysql`: stores processed data  
  - `ingestion`: copies raw CSVs into a shared volume  
  - `processing`: runs a PySpark batch job  
  - `dashboard`: displays processed insights via Streamlit  

- `ingest.py`  
  Ingests raw data by copying CSVs into a shared directory.

- `process_batch.py`  
  PySpark job that:
  - Reads raw CSVs
  - Cleans and transforms the data
  - Aggregates daily ratings and review counts
  - Loads results into the MySQL database

- `app.py`  
  Streamlit dashboard showing summarized data per establishment and state.

## Requirements

- Docker & Docker Compose
- Python 3.8+
- PySpark
- Winutils (if running Spark locally on Windows)

## How to Run

### 1. Build and start the full pipeline:

  ```bash
  docker-compose up --build
  ```

### 2. The dashboard will be available at:
  ```
  http://localhost:8501
  ```

## Before Running

### 1. Create the target MySQL table

Connect to the MySQL container:

```bash
docker exec -it batch_mysql mysql -u batch_user -p batch_db
```

Inside MySQL, create the table:

```sql
CREATE TABLE daily_establishment_data (
    organization VARCHAR(255),
    state VARCHAR(50),
    date DATE,
    avg_rating DECIMAL(3, 2),
    avg_num_reviews DECIMAL(10, 2),
    processing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Prepare Raw Data

Place your raw CSV files in the folder:

```bash
ingestion/source_data/
```

They will be automatically copied to the shared ```/shared``` volume by the ingestion service.

### 3. Schedule the Batch Job

To automate weekly runs:

- Open Task Scheduler
- Create a new task with:
  - Trigger: Weekly (e.g., every Monday at 2 AM)
  - Action: Run ```docker-compose up --build``` inside the project directory

This ensures the full pipeline re-executes with new data.

## Repository

All source codes are available at:  
[https://github.com/Joel-Kazadi/Batch-Processing-System-for-Service-Recommendations](https://github.com/Joel-Kazadi/Batch-Processing-System-for-Service-Recommendations)

## Author

- Joël K. Kazadi, MSc. Data Science, International University of Applied Sciences
