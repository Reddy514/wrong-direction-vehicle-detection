from ultralytics import YOLO
from core.config import YOLO_MODEL, YOLO_CLASSES

class VehicleDetector:
    def __init__(self):
        self.model = YOLO(YOLO_MODEL)
        self.class_names = self.model.names

    def track(self, frame):
        # Only track specified classes (car, motorcycle, bus, truck)
        return self.model.track(frame, persist=True, classes=YOLO_CLASSES, verbose=False)
