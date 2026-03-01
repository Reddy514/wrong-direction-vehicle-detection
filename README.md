# AI Wrong Direction Vehicle Detection System

A complete AI-based system using **YOLOv8** for real-time vehicle detection and tracking, spatial coordinate analysis for wrong-way movement detection, and **EasyOCR** for automatic number plate recognition (ANPR). Designed for modularity, optimized performance, and easy deployment on laptops or edge devices like the Raspberry Pi 5.

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
                                                       Yes     No -> (Continue to next frame)
                                                       /
+------------------+     +-------------------+     +------------------+
| Database Module  | <-- | OCR Engine        | <-- | Image Cropper    |
| (SQLite + Logger)|     | (EasyOCR extracts |     | (Saves violation |
+------------------+     |  license plate)   |     |  evidence image) |
                         +-------------------+     +------------------+
```

## Folder Structure
- `core/`
  - `config.py` - All system configurations (thresholds, model paths, etc.)
  - `detector.py` - Wraps YOLOv8 logic.
  - `tracker.py` - Manages ID persistence and spatial centroid history.
  - `direction.py` - Performs mathematical validation for allowed vs wrong trajectories.
  - `ocr.py` - Integrates EasyOCR for plate recognition.
- `utils/`
  - `database.py` - SQLite operations.
  - `logger.py` - Standardized console logging.
- `main.py` - The main orchestrator connecting all modules and running the OpenCV video loop.
- `requirements.txt` - Required environment dependencies.
- `violations/` - Dynamically generated folder storing evidence crops.

## Installation Instructions

### Windows (Laptop / Desktop)
1. **Clone the repo** and navigate to the root directory.
2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run**:
   ```bash
   python main.py
   ```
   *Note: On the first run, YOLOv8n and EasyOCR models will be downloaded automatically.*

### Raspberry Pi 5 Deployment 
For edge deployment, the workflow is similar but requires installing optimized versions of OpenCV and PyTorch.
1. Increase swap size to 4GB to handle model loading.
2. Create a virtual environment (`python3 -m venv venv --system-site-packages`).
3. Install system packages for OpenCV: `sudo apt-get install python3-opencv`.
4. Install exactly `pip install -r requirements.txt`.
5. In `core/config.py`, consider setting `YOLO_MODEL = 'yolov8n.pt'` to an NCNN or TFLite exported model for enhanced FPS on ARM architecture. Swap EasyOCR to Tesseract if RAM is highly constrained.

## Workflow Explanation
1. **Frame Capture**: Reads frames via OpenCV (`main.py`).
2. **Detection & Tracking**: YOLOv8 detects classes (car, motorcycle, bus, truck) and assigns consistent IDs across frames using BoT-SORT logic (`detector.py`).
3. **Centroid History**: The center point of the bounding box is logged per frame for each active ID (`tracker.py`).
4. **Vector Validation**: Once enough points are collected (e.g., 10 frames), the angle between the first and last point is calculated. If it falls outside the `ALLOWED_ANGLE` tolerance (`config.py`), it is flagged as a wrong-direction violation (`direction.py`).
5. **Evidence Capture**: On violation, the bounding box area is cropped and saved to the `violations/` directory.
6. **OCR**: EasyOCR scans the cropped image for alphanumeric text to capture the license plate (`ocr.py`).
7. **Logging**: The ID, Timestamp, Class, Plate Number, and Image Path are persisted to a local SQLite database (`database.py`) and alerted via console (`logger.py`).

## Scale & Real-World Improvements
- **Camera Calibration**: Map 2D pixel coordinates to real-world 3D map coordinates to calculate actual speed and more accurate trajectories, accounting for perspective distortion.
- **Region of Interest (RoI)**: Process YOLO inference only on the drivable road polygonal mask to boost processing speed.
- **Dynamic OCR**: Instead of running EasyOCR immediately on the first trigger, capture 5 subsequent frames of the violating vehicle, run OCR on the sharpest (least blurry frame), or vote on the most common character sequence.
- **Model Quantization**: Export YOLOv8 to INT8 TensorRT (Nvidia Jetson) or TFLite/NCNN (Raspberry Pi) for real-time edge performance.
- **Night Vision Support**: Train the YOLO model with infrared (IR) night traffic datasets and use IR-capable IP cameras.

## Interview Q&A
**Q: Why use YOLO's built-in tracking (BoT-SORT) over raw DeepSORT?**
A: YOLOv8 integrated BoT-SORT natively, providing state-of-the-art ReID (Re-Identification) and Kalman filtering directly from the detection inference loop without loading an entirely separate heavy feature-extraction network like classical DeepSORT, making it much faster on CPU.

**Q: How do you handle perspective distortion from different camera angles?**
A: In a production setup, we would implement Homography transforms. We'd select 4 points on the ground plane and warp the object's bottom-center coordinates to a top-down orthogonal view. This maps pixel movement accurately to real-world distance and vectors.

**Q: Why EasyOCR over Tesseract?**
A: EasyOCR uses modern deep learning (CRAFT for text detection, CRNN for recognition) and often provides better accuracy on natural, 'in-the-wild' images with varied fonts and backgrounds compared to Tesseract, which requires strict image binarization pre-processing. Tesseract is lighter, however, and can be used on extremely constrained hardware if required.
