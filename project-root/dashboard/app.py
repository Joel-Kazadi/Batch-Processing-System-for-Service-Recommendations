import streamlit as st
import pandas as pd
import mysql.connector
import os

st.title("Daily Establishment Insights")

MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3307))
MYSQL_DB = os.environ.get("MYSQL_DB", "batch_db")
MYSQL_USER = os.environ.get("MYSQL_USER", "batch_user")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "batch_password")

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

    query = """
        SELECT organization, state, date, avg_rating, avg_num_reviews
        FROM daily_establishment_data
        ORDER BY date DESC
        LIMIT 100
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df)

except Exception as e:
    st.error(f"Could not connect to database: {e}")
