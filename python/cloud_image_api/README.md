# Cloud Image Recognition API

A FastAPI service leveraging Google Cloud Vision API to analyze uploaded images and return detected labels.

## Prerequisites

- Python 3.8+
- Google Cloud service account JSON key

## Installation

1. Clone the repository.
2. Place your Google Cloud service account JSON key in the project directory.
3. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your JSON key.
4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the API

Start the server with:

```bash
uvicorn main:app --reload
```

## Usage

Send a POST request to `/analyze` with an image file.

Example using curl:

```bash
curl -F "file=@your_image.jpg" http://localhost:8000/analyze
```

## License

This project is licensed under the MIT License.
