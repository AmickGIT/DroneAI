import math

import numpy as np
from scipy.special import softmax
from motion_controller import MotionController
from vector_visualisation import VectorVisualisation

class GestureClassifier:
    def __init__(self):
        self.visualisation = VectorVisualisation()

    def classify(self, landmarks):
        """
        Classify gesture based on hand landmarks.

        Simplified logic:
        - "Closed Hand": All fingers are folded.
        - "Open Hand": All fingers are extended.
        - "Unknown Gesture": Any other configuration.
        """
        controller = MotionController()
        index_tip = landmarks.landmark[8]
        index_base = landmarks.landmark[5]
        wrist = landmarks.landmark[0]
        
        

        is_ring_closed = self.is_finger_closed(landmarks, finger_tip_index=16, finger_base_index = 13)
        is_middle_closed = self.is_finger_closed(landmarks, finger_tip_index=12, finger_base_index = 9)
        is_acclerating = self.is_acclerating(landmarks)
        if (not (is_ring_closed or is_middle_closed)) or index_tip.z > -0.1:
            return "STOP"
        else:
            index_vector = self.calculate_index_vector(landmarks)
            direction = self.classify_vector_direction(index_vector)
            return direction

            


    


    def calculate_distance(self, coords1, coords2):
        return math.sqrt((coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2 + (coords1[2]-coords2[2])**2)
    
    def is_finger_closed(self, hand_landmarks, finger_tip_index, finger_base_index):
        finger_tip = hand_landmarks.landmark[finger_tip_index]
        finger_base = hand_landmarks.landmark[finger_base_index]
        distance = self.calculate_distance((finger_tip.x, finger_tip.y, finger_tip.z), (finger_base.x, finger_base.y, finger_tip.z))
        
        return distance < 0.30
    
    def is_acclerating(self, hand_landmarks, thumb_tip_index = 4, index_base_index = 5):
        thumb_tip = hand_landmarks.landmark[thumb_tip_index]
        index_base = hand_landmarks.landmark[index_base_index]
        distance = self.calculate_distance((thumb_tip.x, thumb_tip.y, thumb_tip.z), (index_base.x, index_base.y, index_base.z))

        return "acclerating" if distance > 0.12 else "Constant speed"
    
    def calculate_index_vector(self, landmarks, index_tip_id = 8, index_base_id = 4):
        tip = landmarks.landmark[index_tip_id]
        base = landmarks.landmark[index_base_id]

        direction = np.array([tip.x - base.x, tip.y - base.y, tip.z - base.z])
        magnitude = np.linalg.norm(direction)

        return direction/magnitude if magnitude > 0 else np.zeros(3)   
    
    
    

    

    def classify_vector_direction(self, vector, threshold=0.1):
        """
        Classify the direction of a vector.
        
        :param vector: Input 3D vector [x, y, z].
        :param threshold: Minimum contribution for secondary direction to be included.
        :return: A string representing the direction.
        """
        directions = ["X-axis", "Y-axis", "Z-axis"]
        axis_labels = {
            "X-axis": ["Left", "Right"],
            "Y-axis": ["Down", "Up"],
            "Z-axis": ["Back", "Front"],
        }
        
        # vector = np.array(vector)
        softmaxed_vector = softmax(vector)
        
        # Find the dominant axis
        dominant_axis = np.argmax(softmaxed_vector)
        primary_direction = axis_labels[directions[dominant_axis]][0 if vector[dominant_axis] < 0 else 1]
        
        # Check if secondary contributions are significant
        secondary_axis = np.argsort(softmaxed_vector)[-2]
        if softmaxed_vector[secondary_axis] >= threshold:
            secondary_direction = axis_labels[directions[secondary_axis]][0 if vector[secondary_axis] < 0 else 1]
            return f"{primary_direction} and {secondary_direction}"
        else:
            return primary_direction

   
