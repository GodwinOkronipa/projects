from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
import os
from google.cloud import vision
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

app = FastAPI(title="Cloud Image Recognition API")

# Set your credentials path or use environment variable
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'path/to/credentials.json')

try:
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)
    logging.info("Google Cloud Vision client initialized.")
except Exception as e:
    vision_client = None
    logging.error(f"Failed to initialize Vision client: {e}")

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    if not vision_client:
        raise HTTPException(status_code=500, detail="Vision client not initialized.")
    try:
        contents = await file.read()
        image = vision.Image(content=contents)
        response = vision_client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations]
        logging.info(f"Image analyzed: {labels}")
        return JSONResponse(content={"labels": labels})
    except Exception as e:
        logging.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail="Image analysis failed.")
