# GateKeeper-CV 

GateKeeper-CV is an **Automatic License Plate Recognition (ALPR)** and security management system designed for residential complexes, office parks, and gated communities. It uses computer vision to detect vehicles, read license plates, and cross-reference them against a local database for access control.

## Features

- **Real-time Vehicle Detection**: Powered by **YOLOv8** for high-speed and accurate vehicle localization.
- **Smart OCR**: Utilizes **EasyOCR** for robust text extraction from license plates.
- **Access Control**: Categories vehicles into **RESIDENT**, **VISITOR**, or **BANNED** with instant visual alerts.
- **Audit Trail**: Logs every entry with a timestamp, confidence score, and a high-quality snapshot of the vehicle.
- **Pattern Validation**: Optimized for Ghanaian license plate formats (e.g., `GR-123-22`).
- **Webcam Integration**: Ready to run on any standard webcam or IP camera feed.

## Technology Stack

- **Python 3.10+**
- **OpenCV**: Image processing and video stream handling.
- **Ultralytics (YOLOv8)**: Deep learning object detection.
- **EasyOCR**: Neural network-based Optical Character Recognition.
- **SQLite3**: Lightweight, local persistent storage for vehicle logs and registries.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GodwinOkronipa/projects.git
   cd projects/ai-projects/GateKeeper-CV
   ```

2. **Install Dependencies**:
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Initialization**:
   Populate the database with initial vehicle records:
   ```bash
   python database.py
   ```

## 🚦 Usage

To start the real-time monitoring system:

```bash
python main.py
```

- **Live View**: A window will open showing the camera feed.
- **Visual Feedback**:
  - 🟢 **Green Box**: Resident or Approved Visitor.
  - 🟠 **Orange Box**: Unknown Vehicle.
  - 🔴 **Red Box**: BANNED Vehicle (Warning Alert).
- **Quit**: Press `q` to safely shut down the system.

##  Project Structure

- `main.py`: The heart of the system; handles the video loop and system orchestration.
- `detector.py`: Contains the `GateKeeperDetector` class for YOLOv8 and OCR logic.
- `database.py`: Manages SQLite tables for vehicle registry and entry logs.
- `snapshots/`: Directory where images of detected vehicles are stored.
- `data/`: Contains the `gatekeeper.db` file.

##  Configuration

You can modify the `COOLDOWN` period in `main.py` (default 30s) to prevent duplicate logging of the same vehicle. Plate validation logic can be adjusted in `detector.py` under the `plate_pattern` regex.

##  License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built by Godwin Okronipa*
