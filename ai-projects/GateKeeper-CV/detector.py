import cv2
import torch
import easyocr
import re
import numpy as np
from ultralytics import YOLO

class GateKeeperDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # Load YOLOv8 model (standard Nano version for speed)
        self.model = YOLO(model_path)
        # Initialize EasyOCR Reader for English (and numbers)
        self.reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
        # Regex for Ghanaian plate formats (e.g., GR-550-22, GW-123-23)
        # Format: 2 letters, hyphen, 1-4 digits, hyphen, 2 digits (year)
        # We can be slightly looser: [A-Z]{1,2}\s*-\s*\d{1,4}\s*-\s*\d{2}
        self.plate_pattern = re.compile(r'[A-Z]{1,2}-\d{1,4}-\d{2}')

    def preprocess_crop(self, crop):
        """Preprocesses the crop for better OCR results."""
        # Convert to Grayscale
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        
        # Apply Adaptive Thresholding (Binarization)
        # This helps separate text from the background
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return binary

    def detect_vehicles(self, frame):
        """Detects cars and trucks in the frame."""
        # Class IDs for COCO dataset: 2 = car, 7 = truck
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                if (cls == 2 or cls == 7) and conf > 0.5:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append({
                        'bbox': (x1, y1, x2, y2),
                        'conf': conf,
                        'class': 'Car' if cls == 2 else 'Truck'
                    })
        return detections

    def extract_plate(self, car_crop):
        """Extracts license plate text from a car crop."""
        # Note: OCRing the whole car crop might be noisy.
        # Ideally we'd have a plate detector, but following the baseline spec:
        
        # Preprocess
        processed = self.preprocess_crop(car_crop)
        
        # OCR
        results = self.reader.readtext(processed)
        
        best_plate = None
        max_conf = 0
        
        for (bbox, text, conf) in results:
            # Clean up text (remove spaces, special chars except hyphen)
            clean_text = re.sub(r'[^A-Z0-9-]', '', text.upper())
            
            # Check against regex
            if self.plate_pattern.search(clean_text):
                if conf > max_conf:
                    best_plate = clean_text
                    max_conf = conf
            
        return best_plate, max_conf

    def validate_plate(self, text):
        """Validates if the text matches the plate pattern."""
        if not text:
            return None
        match = self.plate_pattern.search(text)
        return match.group(0) if match else None

if __name__ == "__main__":
    # Test initialization
    detector = GateKeeperDetector()
    print("Detector initialized successfully.")
