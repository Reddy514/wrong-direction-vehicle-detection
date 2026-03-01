# AI Wrong Direction Vehicle Detection System

A complete AI-based system using **YOLOv8** for real-time vehicle detection and tracking, spatial coordinate analysis for wrong-way movement detection, and **EasyOCR** for automatic number plate recognition (ANPR).

## System Architecture

```text
[Video Feed / Camera] 
        |
        v
+------------------+     +-------------------+     +------------------+
| YOLOv8 Detector  | --> | BoT-SORT Tracker  | --> | Direction Module |
| (Detects vechs)  |     | (Assigns IDs &    |     | (Analyzes Vector |
+------------------+     |  keeps history)   |     |  Angles)         |
                         +-------------------+     +------------------+
                                                            |
                                                            v
                                                   [Wrong Way Detected?] 
                                                          /   \
                                                       Yes     No -> (Next Frame)
                                                       /
+------------------+     +-------------------+     +------------------+
| Database Module  | <-- | OCR Engine        | <-- | Image Cropper    |
| (SQLite + Logger)|     | (EasyOCR extracts |     | (Saves violation |
+------------------+     |  license plate)   |     |  evidence image) |
                         +-------------------+     +------------------+
```

## Folder Structure
- `core/`
  - `config.py` - configuration settings.
  - `detector.py` - YOLOv8 logic.
  - `tracker.py` - ID persistence and history.
  - `direction.py` - Trajectory validation.
  - `ocr.py` - EasyOCR integration.
  - `database.py` - SQLite operations.
- `utils/`
  - `logger.py` - Console logging.
- `main.py` - Main orchestrator.
- `requirements.txt` - Dependencies.
- `violations/` - Violation evidence crops.
- `plates/` - License plate crops.

## Installation & Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run**:
   ```bash
   python main.py
   ```
