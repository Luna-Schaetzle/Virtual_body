#Kamera Testen
import cv2

def enumerate_cameras(limit=10):
    available_cameras = []
    for i in range(limit):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print(f"Kamera mit Index {i} nicht verfügbar.")
        else:
            print(f"Kamera mit Index {i} gefunden!")
            available_cameras.append(i)
        cap.release()
    return available_cameras

# Verwende die Funktion, um verfügbare Kameras zu finden
available_cameras = enumerate_cameras()
print("Verfügbare Kameras:", available_cameras)
