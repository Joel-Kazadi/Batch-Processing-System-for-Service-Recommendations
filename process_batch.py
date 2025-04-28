import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, to_date, avg, current_timestamp, trim

# --- Configuration ---
DEFAULT_INPUT_DIR = "E:/Mes cours/IU/Documentation/Semester 2/Data Engineering/Portfolio/dataset"
DEFAULT_OUTPUT_TABLE = "daily_establishment_data"
DEFAULT_ARCHIVE_DIR = "E:/Mes cours/IU/Documentation/Semester 2/Data Engineering/Portfolio/dataset/archive"

MYSQL_HOST = "localhost"
MYSQL_PORT = "3307"  # Use 3306 if you're not remapping it
MYSQL_DB = "batch_db"
MYSQL_USER = "batch_user"
MYSQL_PASSWORD = "batch_password"
JDBC_URL = f"jdbc:mysql://{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
JDBC_PROPERTIES = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "driver": "com.mysql.cj.jdbc.Driver"
}

# --- Argument Parsing ---
parser = argparse.ArgumentParser()
parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
parser.add_argument("--output-table", default=DEFAULT_OUTPUT_TABLE)
args = parser.parse_args()

# --- Spark Session ---
spark = SparkSession.builder \
    .appName("DailyEstablishmentAggregation") \
    .master("local[*]") \
    .config("spark.jars.packages", "mysql:mysql-connector-java:8.0.33") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print(f"Reading data from: {args.input_dir}")
print(f"Writing to MySQL table: {args.output_table}")

try:
    # --- Load Raw Data ---
    df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv(args.input_dir)

    # --- Preprocess & Clean ---
    df_clean = df_raw \
        .withColumn("date", to_date(to_timestamp("Time_GMT"))) \
        .withColumn("rating", col("Rating").cast("double")) \
        .withColumn("num_reviews", col("NumberReview").cast("int")) \
        .withColumn("category", trim(col("Category")))

    # Drop unwanted column if exists
    if "OLF" in df_clean.columns:
        df_clean = df_clean.drop("OLF")

    # --- Aggregate by Establishment, State, Date ---
    df_agg = df_clean.groupBy(
        col("Organization").alias("organization"),
        col("State").alias("state"),
        col("date")
    ).agg(
        avg("rating").alias("avg_rating"),
        avg("num_reviews").alias("avg_num_reviews")
    ).withColumn("processing_timestamp", current_timestamp())

    print(f"Aggregated {df_agg.count()} daily records.")

    if df_agg.count() > 0:
        df_agg.write.jdbc(
            url=JDBC_URL,
            table=args.output_table,
            mode="append",
            properties=JDBC_PROPERTIES
        )
        print("Data written successfully to MySQL.")
    else:
        print("No data to write after aggregation.")

except Exception as e:
    print(f"Error occurred during processing: {e}")
finally:
    spark.stop()
    print("Spark session stopped.")