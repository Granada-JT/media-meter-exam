import pandas as pd
import pymongo
import os
from datetime import datetime

MONGO_URI = "mongodb+srv://granada-jt:mgVK1ngGd6TArn8B@b295.gdrdocw.mongodb.net/medalists_db?retryWrites=true&w=majority"
DB_NAME = "medalists_db"
COLLECTION_NAME = "medalists_events"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Ensure indexing for fast queries
collection.create_index([("event", pymongo.ASCENDING)])
collection.create_index([("name", pymongo.ASCENDING), ("event", pymongo.ASCENDING), ("medal_type", pymongo.ASCENDING)], unique=True)

def process_csv(file_path):
    try:
        # Specify encoding to fix decoding errors
        df = pd.read_csv(file_path, encoding='latin1')
        
        # Ensure required columns exist
        required_columns = {"name", "medal_type", "gender", "country", "country_code", "nationality", "event", "discipline", "medal_date"}
        if not required_columns.issubset(df.columns):
            print(f"Skipping file {file_path}: Missing required columns")
            return
        
        # Transform data (convert date formats, trim spaces)
        df["medal_date"] = pd.to_datetime(df["medal_date"], errors="coerce")
        fill_values = {col: "" if col not in ["medal_code", "code_athlete", "code_team"] else 0 for col in df.columns}
        df.fillna(fill_values, inplace=True)

        # Convert DataFrame to list of dictionaries
        records = df.to_dict(orient="records")

        # Bulk insert while avoiding duplicates
        for record in records:
            try:
                collection.update_one(
                    {"name": record["name"], "event": record["event"], "medal_type": record["medal_type"]},
                    {"$set": record},
                    upsert=True
                )
            except Exception as e:
                print(f"Error inserting record: {e}")

        print(f"File processed successfully: {file_path}")

        # Move processed file to archive
        processed_dir = "storage/app/medalists/processed/"
        os.makedirs(processed_dir, exist_ok=True)
        os.rename(file_path, os.path.join(processed_dir, os.path.basename(file_path)))

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
