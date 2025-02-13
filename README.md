# Medalists API

Medalists API is a FastAPI-based application that provides endpoints for uploading CSV files and retrieving aggregated statistics about medalists. A background service processes the uploaded CSV files and stores the data in a MongoDB database.

## Repository Structure

```
/api       # FastAPI backend for API endpoints
/service   # Background service for processing CSV files
README.md  # Setup and usage instructions
```

## Features

- Upload CSV files containing medalist data.
- Store and index data in a MongoDB collection.
- Retrieve aggregated statistics of events and medalists.
- Automatically process new CSV files using a background watcher service.

## Setup and Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.9+
- MongoDB
- pip (Python package manager)

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Granada-JT/media-meter-exam.git
```

#### Install dependencies for API

```bash
cd api
pip install -r requirements.txt
```

#### Install dependencies for Service

```bash
cd ../service
pip install -r requirements.txt
```

### Configuration

Ask for `.env` file with the following variables:

```
MONGO_URI=mongodb_uri
DB_NAME=db_name
DB_COLLECTION=collection
```

## Running the Application

### Start the API Server

Run the FastAPI application:

```bash
cd api
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Start the Background Service

Run the CSV watcher service:

```bash
cd ../service
python watcher.py
```

This service will automatically process new CSV files placed in `storage/app/medalists/`.

## API Endpoints

### Health Check

```
GET /
Response: {"message": "Medalists API is running"}
```

### Upload a CSV File

```
POST /upload
- Request: Multipart file upload (only CSV allowed)
- Response: { "filename": "file.csv", "message": "File uploaded successfully" }
```

### Get Aggregated Medalist Statistics

```
GET /aggregated_stats/event?page=<page_number>
- Response: Paginated medalists grouped by discipline, event, and date
```

## Assumptions & Design Decisions

- **CSV Format:** The CSV files must contain specific columns (`name`, `medal_type`, `gender`, `country`, `country_code`, `nationality`, `event`, `discipline`, `medal_date`).
- **Pagination:** The statistics endpoint supports pagination with a default page size of 10.
- **Data Deduplication:** The database enforces uniqueness based on `name`, `event`, and `medal_type`.
- **Directory Handling:** The watcher service moves processed files to `storage/app/medalists/processed/`.

## Additional Features

- MongoDB indexing for faster queries.
- Automatic file processing using `watchdog`.
- Exception handling for data inconsistencies.
