import shutil
import os

SOURCE_DIR = "/app/source_data"
DEST_DIR = "/shared"

def ingest():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source folder {SOURCE_DIR} not found.")
        return
    os.makedirs(DEST_DIR, exist_ok=True)
    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".csv"):
            shutil.copy(os.path.join(SOURCE_DIR, file), os.path.join(DEST_DIR, file))
            print(f"Ingested: {file}")

if __name__ == "__main__":
    ingest()