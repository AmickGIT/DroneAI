import cv2
import mediapipe as mp
from gesture_classifier import GestureClassifier  # Import the classifier class

# Initialize Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize Gesture Classifier
classifier = GestureClassifier()

# Start webcam capture
cap = cv2.VideoCapture(0)

# Variable to track the first hand
first_hand_detected = False
first_hand_landmarks = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not capture frame!")
        break

    # Convert to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        # If no hand has been tracked yet, start tracking the first hand
        if not first_hand_detected:
            # Track the first detected hand
            first_hand_landmarks = results.multi_hand_landmarks[0]
            first_hand_detected = True
        
        # Use the first hand detected, if available
        if first_hand_landmarks:
            # Draw landmarks for the first hand
            mp_drawing.draw_landmarks(frame, first_hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect gesture using the classifier for the first hand
            gesture = classifier.classify(first_hand_landmarks)
            cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # If no hands are visible anymore, reset tracking
    if not results.multi_hand_landmarks:
        first_hand_detected = False
        first_hand_landmarks = None

    # Display the video feed
    cv2.imshow('Hand Gesture Recognition', frame)

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Hand Gesture Recognition', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
