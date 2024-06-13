import cv2
import mediapipe as mp

# Initialisiere MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialisiere die Webcam
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

        # Konvertiere das BGR-Bild zu RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Erkenne das Face Mesh
        results = face_mesh.process(image)

        # Zeichne die Face Mesh Annotationen auf das Bild
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Mund-Landmarks
                landmarks = face_landmarks.landmark
                
                # Oberlippe
                upper_lip = [landmarks[i] for i in [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]]
                # Unterlippe
                lower_lip = [landmarks[i] for i in [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]]
                
                # Zeichne die Linien für die Ober- und Unterlippe
                for i in range(len(upper_lip) - 1):
                    cv2.line(image, 
                             (int(upper_lip[i].x * image.shape[1]), int(upper_lip[i].y * image.shape[0])), 
                             (int(upper_lip[i+1].x * image.shape[1]), int(upper_lip[i+1].y * image.shape[0])), 
                             (255, 0, 0), 2)
                
                for i in range(len(lower_lip) - 1):
                    cv2.line(image, 
                             (int(lower_lip[i].x * image.shape[1]), int(lower_lip[i].y * image.shape[0])), 
                             (int(lower_lip[i+1].x * image.shape[1]), int(lower_lip[i+1].y * image.shape[0])), 
                             (255, 0, 0), 2)

                # Verbinde die Enden, um den Mund zu schließen
                cv2.line(image, 
                         (int(upper_lip[0].x * image.shape[1]), int(upper_lip[0].y * image.shape[0])),
                         (int(lower_lip[0].x * image.shape[1]), int(lower_lip[0].y * image.shape[0])),
                         (255, 0, 0), 2)
                cv2.line(image, 
                         (int(upper_lip[-1].x * image.shape[1]), int(upper_lip[-1].y * image.shape[0])),
                         (int(lower_lip[-1].x * image.shape[1]), int(lower_lip[-1].y * image.shape[0])),
                         (255, 0, 0), 2)

        # Zeige das resultierende Frame an
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Drücke 'ESC', um zu beenden
            break

cap.release()
cv2.destroyAllWindows()
