import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe solutions
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh, \
     mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Convert the BGR image to RGB and process it with MediaPipe
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results_face_mesh = face_mesh.process(image)
        results_hands = hands.process(image)

        # Create a black background
        h, w, _ = image.shape
        image = np.zeros((h, w, 3), dtype=np.uint8)

        # Draw simple face and hands landmarks
        if results_face_mesh.multi_face_landmarks:
            for face_landmarks in results_face_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None, 
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1))

        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:   
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=4, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))


        # Display the resulting frame
        cv2.imshow('MediaPipe Face and Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
