import math
from core.config import ALLOWED_ANGLE, ANGLE_TOLERANCE

def calculate_angle(p1, p2):
    """
    Calculate the angle between two points in degrees.
    (0 = right, 90 = down, 180 = left, 270 = up)
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    angle = math.degrees(math.atan2(dy, dx))
    if angle < 0:
        angle += 360
    return angle

def is_wrong_direction(p_start, p_current):
    """
    Determine if movement from p_start to p_current constitutes a wrong direction violation.
    Returns boolean.
    """
    angle = calculate_angle(p_start, p_current)
    
    # Check if angle is outside the allowed bounds
    angle_diff = abs(angle - ALLOWED_ANGLE)
    if angle_diff > 180:
        angle_diff = 360 - angle_diff
        
    return angle_diff > ANGLE_TOLERANCE
