import math
import cv2
import numpy as np


class MotionController():
    def calculate_index_direction(self, landmarks, tip_id = 8, base_id = 4):
        tip = landmarks.landmark[tip_id]
        base = landmarks.landmark[base_id]

        direction = np.array([tip.x - base.x, tip.y - base.y, tip.z - base.z])
        magnitude = np.linalg.norm(direction)
        return direction if magnitude > 0 else np.zeros(3)
    
