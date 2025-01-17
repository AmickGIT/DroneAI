import cv2
import numpy as np
import mediapipe as mp
from gesture_classifier import GestureClassifier


# Initialize Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize Gesture Classifier
classifier = GestureClassifier()


count = 0

# Start webcam capture
cap = cv2.VideoCapture(0)
image = np.zeros((500, 500, 3), dtype=np.uint8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not capture frame!")
        break
    
    frame = cv2.flip(frame, 1)
    # Convert to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect gesture using the classifier
            gesture = classifier.classify(hand_landmarks)    
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    
    # Display the video feed
    cv2.imshow('Hand Gesture Recognition', frame)

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Hand Gesture Recognition', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()

