import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize webcam
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Prepare a blank canvas (green background)
        height, width, _ = image.shape
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        canvas[:] = (0, 0, 0)  # Set the canvas to green

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Detect the face mesh
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the face mesh annotations on the green canvas instead of the image
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    canvas,  # Draw on the green canvas
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

        # Display the resulting frame
        cv2.imshow('MediaPipe Face Mesh', canvas)
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
            break

cap.release()
cv2.destroyAllWindows()
