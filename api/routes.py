from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import pymongo
import os
from dotenv import load_dotenv
import shutil

load_dotenv()

router = APIRouter()

UPLOAD_DIR = "storage/app/medalists/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the directory exists

db_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')
db_collection = os.getenv('DB_COLLECTION')

# Set up MongoDB connection
client = pymongo.MongoClient(db_uri)
db = client[db_name]
collection = db[db_collection]

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "File uploaded successfully"}

@router.get("/aggregated_stats/event")
async def get_event_stats(page: int = Query(1, ge=1)):
    try:
        per_page = 10
        skip = (page - 1) * per_page

        # Aggregation pipeline: group by discipline, event, and medal_date
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "discipline": "$discipline",
                        "event": "$event",
                        "event_date": "$medal_date"
                    },
                    "medalists": {
                        "$push": {
                            "name": "$name",
                            "medal_type": "$medal_type",
                            "gender": "$gender",
                            "country": "$country",
                            "country_code": "$country_code",
                            "nationality": "$nationality",
                            "medal_date": "$medal_date"
                        }
                    }
                }
            },
            { "$sort": { "_id.event_date": 1 } },
            { "$skip": skip },
            { "$limit": per_page }
        ]

        result = list(collection.aggregate(pipeline))
        data = []
        for group in result:
            data.append({
                "discipline": group["_id"]["discipline"],
                "event": group["_id"]["event"],
                "event_date": group["_id"]["event_date"],
                "medalists": group["medalists"]
            })

        # Count total groups for pagination
        count_pipeline = [
            {
                "$group": {
                    "_id": {
                        "discipline": "$discipline",
                        "event": "$event",
                        "event_date": "$medal_date"
                    }
                }
            },
            { "$count": "total" }
        ]
        count_result = list(collection.aggregate(count_pipeline))
        total = count_result[0]["total"] if count_result else 0
        total_pages = (total + per_page - 1) // per_page

        # Build pagination URLs
        base_url = "http://127.0.0.1:8000//aggregated_stats/event?page="
        next_page = base_url + str(page + 1) if page < total_pages else None
        previous_page = base_url + str(page - 1) if page > 1 else None

        return {
            "data": data,
            "paginate": {
                "current_page": page,
                "total_pages": total_pages,
                "next_page": next_page,
                "previous_page": previous_page
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    