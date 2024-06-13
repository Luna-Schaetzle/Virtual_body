import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe solutions
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        # Process the image and detect the pose and face mesh
        results_pose = pose.process(image_rgb)
        results_face_mesh = face_mesh.process(image_rgb)

        # Prepare for drawing
        image_rgb.flags.writeable = True
        image_pose = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        h, w, _ = image_pose.shape
        annotated_image = np.zeros((h, w, 3), dtype=np.uint8) + 255  # White background

        # Draw face mesh on the original image
        if results_face_mesh.multi_face_landmarks:
            for face_landmarks in results_face_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image_pose,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1))

        # Create a face mask based on the pose landmarks
        face_mask = np.zeros((h, w, 3), dtype=np.uint8)
        if results_pose.pose_landmarks:
            nose = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
            nose_coords = (int(nose.x * w), int(nose.y * h))

            shoulders = [
                results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER],
                results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            ]
            shoulder_center = np.mean([[int(shoulder.x * w), int(shoulder.y * h)] for shoulder in shoulders], axis=0).astype(int)

            head_size = np.linalg.norm([shoulders[0].x - shoulders[1].x, shoulders[0].y - shoulders[1].y]) * w

            # Draw face mask as a circle
            cv2.circle(face_mask, tuple(shoulder_center), int(head_size // 2), (255, 255, 255), -1)

        # Mask the face area
        face_area = cv2.bitwise_and(image_pose, face_mask)

        # Draw the body of the stick figure
        if results_pose.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image,
                results_pose.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2))

        # Overlay the face area on the stick figure
        annotated_image = cv2.addWeighted(annotated_image, 1, face_area, 1, 0)

        cv2.imshow('Stickman Character with Face', annotated_image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
