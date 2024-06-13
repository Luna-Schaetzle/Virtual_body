import cv2
import mediapipe as mp
import numpy as np

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

        # Erhalte die Bildabmessungen
        height, width, _ = image.shape
        
        # Erstelle ein leeres Bild mit grünem Hintergrund
        green_background = np.zeros((height, width, 3), dtype=np.uint8)
        green_background[:] = (0, 255, 0)  # Grün

        # Konvertiere das BGR-Bild zu RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Erkenne das Face Mesh
        results = face_mesh.process(image)

        # Zeichne die Face Mesh Annotationen auf das grüne Bild
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Mund-Landmarks
                landmarks = face_landmarks.landmark
                
                # Oberlippe
                upper_lip = [landmarks[i] for i in [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]]
                # Unterlippe
                lower_lip = [landmarks[i] for i in [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]]
                
                # Zeichne die Linien für die Ober- und Unterlippe auf das grüne Bild
                def draw_lip(lip, img):
                    points = [(int(point.x * img.shape[1]), int(point.y * img.shape[0])) for point in lip]
                    cv2.polylines(img, [np.array(points)], isClosed=True, color=(255, 0, 0), thickness=2)
                
                draw_lip(upper_lip, green_background)
                draw_lip(lower_lip, green_background)

        # Zeige das resultierende Frame an
        cv2.imshow('MediaPipe Face Mesh', green_background)
        if cv2.waitKey(5) & 0xFF == 27:  # Drücke 'ESC', um zu beenden
            break

cap.release()
cv2.destroyAllWindows()