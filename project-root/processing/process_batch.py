import os
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, to_date, avg, current_timestamp, trim

# --- Configuration ---
INPUT_DIR = "/shared"
OUTPUT_TABLE = "daily_establishment_data"

MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3307")
MYSQL_DB = os.environ.get("MYSQL_DB", "batch_db")
MYSQL_USER = os.environ.get("MYSQL_USER", "batch_user")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "batch_password")

JDBC_URL = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
JDBC_PROPERTIES = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "driver": "com.mysql.cj.jdbc.Driver"
}

spark = SparkSession.builder \
    .appName("DockerSparkBatchProcessing") \
    .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.33") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

try:
    df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv(INPUT_DIR)

    df_clean = df_raw \
        .withColumn("date", to_date(to_timestamp("Time_GMT"))) \
        .withColumn("rating", col("Rating").cast("double")) \
        .withColumn("num_reviews", col("NumberReview").cast("int")) \
        .withColumn("category", trim(col("Category")))

    if "OLF" in df_clean.columns:
        df_clean = df_clean.drop("OLF")

    df_agg = df_clean.groupBy(
        col("Organization").alias("organization"),
        col("State").alias("state"),
        col("date")
    ).agg(
        avg("rating").alias("avg_rating"),
        avg("num_reviews").alias("avg_num_reviews")
    ).withColumn("processing_timestamp", current_timestamp())

    df_agg.write.jdbc(
        url=JDBC_URL,
        table=OUTPUT_TABLE,
        mode="append",
        properties=JDBC_PROPERTIES
    )
    print("Data written to MySQL.")

except Exception as e:
    print(f"Processing error: {e}")

finally:
    spark.stop()
