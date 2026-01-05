import cv2
import os
import time
from database import init_db, get_vehicle_status, log_entry
from detector import GateKeeperDetector

def main():
    # Initialize Database
    init_db()
    
    # Initialize Detector
    print("Loading AI Models... (this may take a minute)")
    detector = GateKeeperDetector()
    
    # Ensure snapshots directory exists
    SNAPSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'snapshots')
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    
    # Open Webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("GateKeeper ALPR System Started. Press 'q' to quit.")
    
    # Track detected plates to avoid duplicate logs in short bursts
    recent_detections = {} # {plate: last_seen_timestamp}
    COOLDOWN = 30 # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        display_frame = frame.copy()
        
        # Step 1: Detect Vehicles
        detections = detector.detect_vehicles(frame)
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            
            # Step 2: Crop Car
            # Add small padding if possible
            h, w, _ = frame.shape
            pad = 10
            cx1, cy1 = max(0, x1-pad), max(0, y1-pad)
            cx2, cy2 = min(w, x2+pad), min(h, y2+pad)
            car_crop = frame[cy1:cy2, cx1:cx2]
            
            if car_crop.size == 0:
                continue
                
            # Step 3: Read Plate
            plate_text, ocr_conf = detector.extract_plate(car_crop)
            valid_plate = detector.validate_plate(plate_text)
            
            if valid_plate:
                # Step 4: Validate and Log
                owner, status = get_vehicle_status(valid_plate)
                
                # Check cooldown
                current_time = time.time()
                if valid_plate not in recent_detections or (current_time - recent_detections[valid_plate]) > COOLDOWN:
                    
                    # Save snapshot
                    timestamp_str = time.strftime("%Y%m%d_%H%M%S")
                    snap_name = f"{valid_plate}_{timestamp_str}.jpg"
                    snap_path = os.path.join(SNAPSHOTS_DIR, snap_name)
                    cv2.imwrite(snap_path, car_crop)
                    
                    # Log to DB
                    log_entry(valid_plate, ocr_conf, snap_path)
                    recent_detections[valid_plate] = current_time
                    
                    print(f"Detected: {valid_plate} | Status: {status} | Owner: {owner}")
                    
                    if status == 'BANNED':
                        print(f"!!! ALERT: BANNED VEHICLE DETECTED: {valid_plate} !!!")

                # Step 5: Draw UI Elements
                color = (0, 255, 0) # Green for Residents/Visitors
                if status == 'BANNED':
                    color = (0, 0, 255) # Red for Banned
                elif status == 'UNKNOWN':
                    color = (255, 165, 0) # Orange for Unknown
                
                # Draw box around car
                cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw Plate Text
                label = f"{valid_plate} ({status})"
                cv2.putText(display_frame, label, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Show the frame
        cv2.imshow('GateKeeper ALPR System', display_frame)
        
        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print("System Shutdown.")

if __name__ == "__main__":
    main()
