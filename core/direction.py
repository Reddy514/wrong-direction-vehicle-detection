import math
from core.config import ALLOWED_ANGLE, ANGLE_TOLERANCE

def is_wrong_direction(p_start, p_current):
    # Calculate vector angle
    dx = p_current[0] - p_start[0]
    dy = p_current[1] - p_start[1]
    
    # math.atan2(dy, dx) returns angle in radians (-pi to pi)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    # Map to 0-360 range (0=Right, 90=Down, 180=Left, 270=Up)
    # OpenCV (0,0) is top-left, so 0=Right, 90=Down, 180=Left, 270=Up.
    angle_deg = (angle_deg + 360) % 360
    
    # Check if angle is within the allowed range
    diff = abs(angle_deg - ALLOWED_ANGLE)
    if diff > 180:
        diff = 360 - diff
        
    return diff > ANGLE_TOLERANCE
