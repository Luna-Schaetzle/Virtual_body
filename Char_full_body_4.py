import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe solutions
mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh, \
     mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Prepare the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #flip image
        image = cv2.flip(image, 1)


        # Process it with MediaPipe
        results_pose = pose.process(image)
        results_face_mesh = face_mesh.process(image)
        results_hands = hands.process(image)

        # Prepare for drawing
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        h, w, _ = image.shape
        annotated_image = np.zeros((h, w, 3), dtype=np.uint8)

        # Draw the 2D avatar based on the pose landmarks and Hand landmarks and Face landmarks
        # Hand landmarks
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=30, circle_radius=2))
                
        # Face landmarks
        if results_face_mesh.multi_face_landmarks:
            for face_landmarks in results_face_mesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1))


        # Draw the pose annotations on the character
        if results_pose.pose_landmarks:
            landmarks = results_pose.pose_landmarks.landmark

        
            # Draw lines for the body (using shoulders, elbows, hips, and knees)
            # Example: Line between left shoulder and left elbow
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            cv2.line(annotated_image, 
                     (int(left_shoulder.x * w), int(left_shoulder.y * h)), 
                     (int(left_elbow.x * w), int(left_elbow.y * h)), 
                     (0, 255, 0), 50)  # Green line for left arm

            # You can continue to draw more lines for other body parts in a similar way

            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            cv2.line(annotated_image, 
                     (int(right_shoulder.x * w), int(right_shoulder.y * h)), 
                     (int(right_elbow.x * w), int(right_elbow.y * h)), 
                     (0, 255, 0), 50)
            
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            cv2.line(annotated_image, 
                     (int(left_hip.x * w), int(left_hip.y * h)), 
                     (int(left_knee.x * w), int(left_knee.y * h)), 
                     (0, 255, 0), 50)
            
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            cv2.line(annotated_image, 
                     (int(right_hip.x * w), int(right_hip.y * h)), 
                     (int(right_knee.x * w), int(right_knee.y * h)), 
                     (0, 255, 0), 50)
            
            # draw Body
            cv2.line(annotated_image, 
                     (int(left_shoulder.x * w), int(left_shoulder.y * h)), 
                     (int(right_shoulder.x * w), int(right_shoulder.y * h)), 
                     (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(left_hip.x * w), int(left_hip.y * h)),
                        (int(right_hip.x * w), int(right_hip.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(left_shoulder.x * w), int(left_shoulder.y * h)),
                        (int(left_hip.x * w), int(left_hip.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_shoulder.x * w), int(right_shoulder.y * h)),
                        (int(right_hip.x * w), int(right_hip.y * h)),
                        (0, 255, 0), 50)
            
            # draw legs
            cv2.line(annotated_image,
                        (int(left_knee.x * w), int(left_knee.y * h)),
                        (int(left_hip.x * w), int(left_hip.y * h)),
                        (0, 255, 0), 50)
            
            cv2.line(annotated_image,
                        (int(right_knee.x * w), int(right_knee.y * h)),
                        (int(right_hip.x * w), int(right_hip.y * h)),
                        (0, 255, 0), 50)
            
            # draw feet
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
            cv2.line(annotated_image,
                        (int(left_knee.x * w), int(left_knee.y * h)),
                        (int(left_ankle.x * w), int(left_ankle.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_knee.x * w), int(right_knee.y * h)),
                        (int(right_ankle.x * w), int(right_ankle.y * h)),
                        (0, 255, 0), 50)
            
            # draw lower arms
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            cv2.line(annotated_image,
                        (int(left_elbow.x * w), int(left_elbow.y * h)),
                        (int(left_wrist.x * w), int(left_wrist.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_elbow.x * w), int(right_elbow.y * h)),
                        (int(right_wrist.x * w), int(right_wrist.y * h)),
                        (0, 255, 0), 50)
            
            # draw conecting lines
            cv2.line(annotated_image,
                        (int(left_shoulder.x * w), int(left_shoulder.y * h)),
                        (int(left_elbow.x * w), int(left_elbow.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_shoulder.x * w), int(right_shoulder.y * h)),
                        (int(right_elbow.x * w), int(right_elbow.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(left_hip.x * w), int(left_hip.y * h)),
                        (int(left_knee.x * w), int(left_knee.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_hip.x * w), int(right_hip.y * h)),
                        (int(right_knee.x * w), int(right_knee.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(left_knee.x * w), int(left_knee.y * h)),
                        (int(left_ankle.x * w), int(left_ankle.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_knee.x * w), int(right_knee.y * h)),
                        (int(right_ankle.x * w), int(right_ankle.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(left_elbow.x * w), int(left_elbow.y * h)),
                        (int(left_wrist.x * w), int(left_wrist.y * h)),
                        (0, 255, 0), 50)
            cv2.line(annotated_image,
                        (int(right_elbow.x * w), int(right_elbow.y * h)),
                        (int(right_wrist.x * w), int(right_wrist.y * h)),
                        (0, 255, 0), 50)
            

                     



        # Display the resulting frame
        cv2.imshow('2D Avatar Animation', annotated_image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
