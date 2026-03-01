from ultralytics import YOLO
from core.config import YOLO_MODEL, YOLO_CLASSES

class VehicleDetector:
    def __init__(self):
        # Initialize YOLO model
        self.model = YOLO(YOLO_MODEL)
        self.classes = YOLO_CLASSES
        self.class_names = self.model.names

    def track(self, frame):
        """
        Run YOLOv8 tracking on a given frame.
        We use built-in tracking (persist=True) which defaults to BoT-SORT/ByteTrack.
        """
        results = self.model.track(
            frame, 
            persist=True, 
            classes=self.classes, 
            verbose=False
        )
        return results
