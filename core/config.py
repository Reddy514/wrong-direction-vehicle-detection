import os

# Paths and Files
VIDEO_SOURCE = r"C:\reactprojects\ai detection\traffic.mp4"  # 0 for webcam, or path to MP4 (e.g., "test_video.mp4")
DB_PATH = "violations.db"
VIOLATIONS_DIR = "violations"
PLATES_DIR = "plates"

# YOLO settings
YOLO_MODEL = 'yolov8n.pt'
YOLO_CLASSES = [2, 3, 5, 7]  # COCO indices for car, motorcycle, bus, truck

# Direction settings
# Allowed direction angle in degrees (0 = right, 90 = down, 180 = left, 270 = up)
ALLOWED_ANGLE = 90
ANGLE_TOLERANCE = 45  # Degrees
MIN_DIST_FOR_DIRECTION = 50  # Minimum pixel distance to consider movement

# Tracker settings
MAX_TRACK_HISTORY = 30
MIN_TRACK_HISTORY_FOR_DIRECTION = 10

# OCR settings
OCR_LANG = ['en']
OCR_GPU = False  # Set False for laptop CPU; Set True if you have Nvidia GPU
OCR_CONF_THRESHOLD = 0.6
