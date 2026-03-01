import cv2
import os
import math
import sys
from core.config import VIDEO_SOURCE, VIOLATIONS_DIR, MIN_DIST_FOR_DIRECTION
from core.detector import VehicleDetector
from core.tracker import TrackerManager
from core.direction import is_wrong_direction
from core.ocr import LicensePlateReader
from core.database import init_db, insert_violation
from utils.logger import get_logger
import re

logger = get_logger("AIDetectorMain")

def main():
    logger.info("Initializing system components...")
    
    # Ensure directories and DB exist
    os.makedirs(VIOLATIONS_DIR, exist_ok=True)
    init_db()

    # Initialize Modules
    try:
        detector = VehicleDetector()
        tracker = TrackerManager()
        ocr_reader = LicensePlateReader()
        logger.info("Models loaded successfully. (Ready for inference)")
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        sys.exit(1)

    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        logger.error(f"Cannot open video source: {VIDEO_SOURCE}")
        sys.exit(1)

    logger.info("Starting video processing loop. Press 'q' to quit.")

    while True:
        success, frame = cap.read()
        if not success:
            logger.info("End of video stream or cannot read frame.")
            break

        # 1. Detection & Tracking
        results = detector.track(frame)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()

            for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                x1, y1, x2, y2 = map(int, box)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                # 2. Update tracking history
                tracker.update(track_id, (cx, cy))
                
                # Draw standard tracking box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                history = tracker.get_history(track_id)

                # 3. Analyze Direction
                if len(history) >= 10:
                    p_start = history[0]
                    p_current = history[-1]
                    
                    dist = math.hypot(p_current[0] - p_start[0], p_current[1] - p_start[1])
                    
                    if dist > MIN_DIST_FOR_DIRECTION:
                        if is_wrong_direction(p_start, p_current):
                            # Visual Alert
                            cv2.putText(frame, "WRONG WAY!", (x1, y1 - 30), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            
                            # 4. Handle Violation (OCR + DB Logging)
                            if not tracker.is_logged(track_id):
                                tracker.mark_logged(track_id)
                                
                                # Crop image for OCR
                                crop = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
                                
                                plate_text = ""
                                plate_conf = 0.0
                                img_path = os.path.join(VIOLATIONS_DIR, f"violation_{track_id}.jpg")
                                
                                if crop.size > 0:
                                    # Run OCR
                                    plate_text, plate_conf = ocr_reader.read_plate(crop)
                                    # Save evidence image
                                    cv2.imwrite(img_path, crop)
                                
                                vehicle_class_name = detector.class_names[class_id]
                                
                                logger.warning(f"VIOLATION: ID {track_id} | Class {vehicle_class_name} | "
                                               f"Plate {plate_text} (Conf: {plate_conf:.2f})")

                                if plate_text and plate_conf > 0.6:
                                    pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$'
                                    if re.match(pattern, plate_text):
                                        insert_violation(track_id, vehicle_class_name, plate_text, plate_conf)
                                        
                                        # Save plate crop image
                                        os.makedirs("plates", exist_ok=True)
                                        plate_image_path = f"plates/{track_id}_{plate_text}.jpg"
                                        cv2.imwrite(plate_image_path, crop)

        # Display Frame
        cv2.imshow("AI Wrong Direction Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("System shutting down properly.")

if __name__ == "__main__":
    main()
