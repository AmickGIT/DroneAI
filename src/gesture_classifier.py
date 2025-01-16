import math


class GestureClassifier:
    def classify(self, landmarks):
        """
        Classify gesture based on hand landmarks.

        Simplified logic:
        - "Closed Hand": All fingers are folded.
        - "Open Hand": All fingers are extended.
        - "Unknown Gesture": Any other configuration.
        """
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        folded_fingers = []
        wrist = landmarks.landmark[0]
        

        is_ring_closed = self.is_finger_closed(landmarks, finger_tip_index=16, finger_base_index = 13)
        if is_ring_closed:
            return "Closed"
        else:
            return "Open"
        # is_pinky_closed = self.is_finger_closed(landmarks, finger_base_index=20, finger_base_index = 0)

        wrist_coords = {
            'x': wrist.x,
            'y': wrist.y,
            'z': wrist.z
        }
        



        for tip_id in finger_tips:
            if (landmarks.landmark[tip_id]) :
                folded_fingers.append(False)  # Finger is extended
            elif(landmarks.landmark[tip_id]):
                folded_fingers.append(True)   # Finger is folded
             


        if all(folded_fingers):
            return f"Closed Hand"
        elif not any(folded_fingers):
            return f"Open Hand"
        else:
            return "Unknown Gesture"


    def calculate_index_direction(landmarks, tip_id = 8, base_id = 4):
        tip = landmarks.landmark[tip_id]
        base = landmarks.landmark[base_id]

        direction = {
            'x': tip.x - base.x,
            'y': tip.y - base.y,
            'z': tip.z - base.z
        }

        
        magnitude = math.sqrt(direction['x']**2 + direction['y']**2 + direction['z']**2)
        if magnitude > 0:
            direction['x'] /= magnitude
            direction['y'] /= magnitude
            direction['z'] /= magnitude

        return direction


    def calculate_distance(self, coords1, coords2):
        return math.sqrt((coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2 + (coords1[2]-coords2[2])**2)
    
    def is_finger_closed(self, hand_landmarks, finger_tip_index, finger_base_index):
        finger_tip = hand_landmarks.landmark[finger_tip_index]
        finger_base = hand_landmarks.landmark[finger_base_index]
        distance = self.calculate_distance((finger_tip.x, finger_tip.y, finger_tip.z), (finger_base.x, finger_base.y, finger_tip.z))
        
        return distance < 0.15