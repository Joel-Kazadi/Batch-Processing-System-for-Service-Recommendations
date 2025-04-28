# Batch-Processing-System-for-Service-Recommendations

## Overview

This project implements a batch-processing-based data architecture to ingest, clean, and aggregate establishment data across different U.S. states. The system is designed to support a machine learning application and a dashboard for recommending establishments to potential customers based on services offered and location.

The architecture uses:
- Docker Compose to set up a MySQL database
- PySpark to perform daily aggregation and preprocessing of establishment data

## Components

- `docker-compose-mysql.yml`  
  Defines a Docker service that runs a MySQL database (`batch_db`) to store processed establishment data.

- `process_batch.py`  
  PySpark batch job script that:
  - Reads raw CSV data
  - Cleans and transforms the data
  - Aggregates daily ratings and review counts per establishment and state
  - Writes the results into the MySQL database

## Requirements

- Docker and Docker Compose
- Python 3.8+
- PySpark
- MySQL Connector JAR for Spark
- Winutils (for running Spark on Windows)

## How to Run

1. Start the MySQL container:

    ```
    docker-compose -f docker-compose-mysql.yml up -d
    ```

2. Run the batch processing script:

    ```
    python process_batch.py --input-dir "path_to_the_csv_folder"
    ```

## Repository

All source codes are available at:  
[https://github.com/Joel-Kazadi/Batch-Processing-System-for-Service-Recommendations](https://github.com/Joel-Kazadi/Batch-Processing-System-for-Service-Recommendations)

## Author

- Joël Kazadi
