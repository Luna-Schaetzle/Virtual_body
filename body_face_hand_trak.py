import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe solutions
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize webcam
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh, \
     mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands, \
     mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        # Detect face mesh, hands, and pose
        results_face_mesh = face_mesh.process(image_rgb)
        results_hands = hands.process(image_rgb)
        results_pose = pose.process(image_rgb)
        
        # Prepare a unified background
        height, width, _ = image.shape
        unified_background = np.zeros((height, width, 3), dtype=np.uint8)
        unified_background[:] = (255, 255, 255)  # Set background to white for visibility

        # Draw only the face mesh on the original image
        if results_face_mesh.multi_face_landmarks:
            for face_landmarks in results_face_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        
        # Copy the face area to the unified background
        unified_background[0:height, 0:width] = image
        
        # Draw hand annotations on the unified background
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    unified_background,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                )
        
        # Draw pose annotations on the unified background
        if results_pose.pose_landmarks:
            mp_drawing.draw_landmarks(
                unified_background,
                results_pose.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
            )

        # Display the resulting frame
        cv2.imshow('Unified Tracking - Face, Hands, and Pose', unified_background)
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
            break

cap.release()
cv2.destroyAllWindows()
