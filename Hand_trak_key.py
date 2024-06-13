import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Keyboard layout definition
keyboard_buttons = {'a': {'top_left': (100, 50), 'bottom_right': (200, 150), 'color': (255, 0, 0)},
                    'b': {'top_left': (300, 50), 'bottom_right': (400, 150), 'color': (0, 255, 0)},
                    'c': {'top_left': (500, 50), 'bottom_right': (600, 150), 'color': (0, 0, 255)},
                    'd': {'top_left': (100, 200), 'bottom_right': (200, 300), 'color': (255, 255, 0)},
                    'e': {'top_left': (300, 200), 'bottom_right': (400, 300), 'color': (255, 0, 255)},
                    'f': {'top_left': (500, 200), 'bottom_right': (600, 300), 'color': (0, 255, 255)},
                    'g': {'top_left': (100, 350), 'bottom_right': (200, 450), 'color': (192, 192, 192)},
                    'h': {'top_left': (300, 350), 'bottom_right': (400, 450), 'color': (128, 128, 128)},
                    'i': {'top_left': (500, 350), 'bottom_right': (600, 450), 'color': (64, 64, 64)}

                    }

# Function to check if a point is inside a rectangle
def is_over_button(point, button):
    x, y = point
    if button['top_left'][0] < x < button['bottom_right'][0] and button['top_left'][1] < y < button['bottom_right'][1]:
        return True
    return False

# Initialize MediaPipe Hands
cap = cv2.VideoCapture(0)

with mp_hands.Hands(model_complexity=0,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Spiegele das Bild horizontal für eine Selfie-Ansicht
        image = cv2.flip(image, 1)

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Convert back to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the keyboard buttons
        for key, value in keyboard_buttons.items():
            cv2.rectangle(image, value['top_left'], value['bottom_right'], value['color'], cv2.FILLED)
            cv2.putText(image, key, (value['top_left'][0] + 40, value['top_left'][1] + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Process hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the tip of the index finger
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_tip_x, index_tip_y = int(index_finger_tip.x * image.shape[1]), int(index_finger_tip.y * image.shape[0])

                # Check if the index finger tip is over any button
                for key, value in keyboard_buttons.items():
                    if is_over_button((index_tip_x, index_tip_y), value):
                        print(f"Pressed: {key}")
                        cv2.rectangle(image, value['top_left'], value['bottom_right'], (255, 255, 255), cv2.FILLED)
                        cv2.putText(image, key, (value['top_left'][0] + 40, value['top_left'][1] + 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                        break

        # Display the resulting image
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
