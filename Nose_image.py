import cv2
import mediapipe as mp

# Initialisiere MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Lade das Bild, das auf die Nase gelegt werden soll
# Ersetze 'Pfad_zum_Bild' mit dem tatsächlichen Pfad zum Bild
image_to_overlay_path = r'C:\Users\Admin\Desktop\Desk\UC_Projekte_4BHWII\ML_1\Kaese_verdienstkreuz.jpg'

image_to_overlay = cv2.imread(image_to_overlay_path)
if image_to_overlay is None:
    print(f"Das Bild unter {image_to_overlay_path} konnte nicht geladen werden.")
else:
    resized_image = cv2.resize(image_to_overlay, (100, 100))  # Beispielgröße


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
                # Finde die Nasenspitze
                nose_tip = face_landmarks.landmark[4]
                x = int(nose_tip.x * image.shape[1]) - resized_image.shape[1] // 2
                y = int(nose_tip.y * image.shape[0]) - resized_image.shape[0] // 2

                # Stelle sicher, dass das Bild nicht über den Rand des Frames hinausgeht
                h, w, _ = resized_image.shape
                if x + w > image.shape[1]:
                    x = image.shape[1] - w
                if y + h > image.shape[0]:
                    y = image.shape[0] - h
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0

                # Bild auf den Frame zeichnen
                image[y:y+h, x:x+w] = resized_image

        # Zeige das resultierende Frame an
        cv2.imshow('MediaPipe Face Mesh', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Drücke 'ESC', um zu beenden
            break

cap.release()
cv2.destroyAllWindows()
