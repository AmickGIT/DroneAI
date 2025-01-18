import math
import numpy as np
from vector_visualisation import VectorVisualisation

class GestureClassifier:
    def __init__(self):
        self.visualisation = VectorVisualisation()

    def enhanced_softmax(self, values, beta=2):
        exp_values = np.exp(beta * values)
        return exp_values / np.sum(exp_values)

    def classify(self, landmarks):
        
        index_tip = landmarks.landmark[8]
       
        is_ring_closed = self.is_finger_closed(landmarks, finger_tip_index=16, finger_base_index = 13)
        is_middle_closed = self.is_finger_closed(landmarks, finger_tip_index=12, finger_base_index = 9)
        is_acclerating = self.is_acclerating(landmarks)
        if (not (is_ring_closed or is_middle_closed)):
            return "STOP"
        elif(index_tip.z > -0.09):
            return "Out of Range"
        else:
            index_vector = self.calculate_index_vector(landmarks)
            direction = self.classify_vector_direction(index_vector)
            return f"{direction} and {is_acclerating}"

    def calculate_distance(self, coords1, coords2):
        return math.sqrt((coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2 + (coords1[2]-coords2[2])**2)
    
    def is_finger_closed(self, hand_landmarks, finger_tip_index, finger_base_index):
        finger_tip = hand_landmarks.landmark[finger_tip_index]
        finger_base = hand_landmarks.landmark[finger_base_index]
        distance = self.calculate_distance((finger_tip.x, finger_tip.y, finger_tip.z), (finger_base.x, finger_base.y, finger_tip.z))
        
        return distance < 0.35
    
    def is_acclerating(self, hand_landmarks, thumb_tip_index = 4, index_base_index = 5, middle_joint_index = 10):
        thumb_tip = hand_landmarks.landmark[thumb_tip_index]
        index_base = hand_landmarks.landmark[index_base_index]
        middle_joint = hand_landmarks.landmark[middle_joint_index]
        distance_from_index_base = self.calculate_distance((thumb_tip.x, thumb_tip.y, thumb_tip.z), (index_base.x, index_base.y, index_base.z))
        distance_from_middle_joint = self.calculate_distance((thumb_tip.x, thumb_tip.y, thumb_tip.z), (middle_joint.x, middle_joint.y, middle_joint.z))
        
        return "constant speed" if (distance_from_index_base < 0.15 or distance_from_middle_joint < 0.15) else "acclerating"
    
    def calculate_index_vector(self, landmarks, index_tip_id = 8, index_base_id = 5):
        tip = landmarks.landmark[index_tip_id]
        base = landmarks.landmark[index_base_id]

        direction = np.array([tip.x - base.x, base.y - tip.y, base.z - tip.z])
        magnitude = np.linalg.norm(direction)
        # print(direction)

        return direction/magnitude 
    
    def classify_vector_direction(self, vector, threshold=0.20):
        directions = ["X-axis", "Y-axis", "Z-axis"]
        axis_labels = {
            "X-axis": ["Left", "Right"],
            "Y-axis": ["Down", "Up"],
            "Z-axis": ["Back", "Front"],
        }
        

        softmaxed_vector = self.enhanced_softmax(np.abs(vector))
        
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

   
