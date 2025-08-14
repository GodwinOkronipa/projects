# Cloud Image Recognition API

This is a FastAPI-based service that uses Google Cloud Vision API to analyze uploaded images and return detected labels.

## Setup
1. Place your Google Cloud service account JSON in this folder and update the path in `main.py` or set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   uvicorn main:app --reload
   ```

## Usage
Send a POST request to `/analyze` with an image file using a tool like curl or Postman.

Example with curl:
```bash
curl -F "file=@your_image.jpg" http://localhost:8000/analyze
```
