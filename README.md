# Virtual_body

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![GitHub last commit](https://img.shields.io/github/last-commit/Luna-Schaetzle/Virtual_body)
![GitHub contributors](https://img.shields.io/github/contributors/Luna-Schaetzle/Virtual_body)
![GitHub issues](https://img.shields.io/github/issues/Luna-Schaetzle/Virtual_body)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Luna-Schaetzle/Virtual_body)
![GitHub repo size](https://img.shields.io/github/repo-size/Luna-Schaetzle/Virtual_body)
![GitHub push](https://img.shields.io/github/commit-activity/m/Luna-Schaetzle/Virtual_body)

Willkommen zu Virtual_body, einem Projekt, das es Ihnen ermöglicht, eine virtuelle Version von sich selbst zu erstellen. Dieses Projekt verwendet verschiedene Python-Skripte, um Masken auf Gesichter, Körper und Hände anzuwenden, sowie zur Erkennung und Verfolgung von Gesichtszügen und Handbewegungen.

## Inhaltsverzeichnis

- [Virtual\_body](#virtual_body)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Programme in der Übersicht](#programme-in-der-übersicht)
  - [Installation](#installation)
  - [Verwendung](#verwendung)
  - [Projektbeschreibung](#projektbeschreibung)
  - [Geplante Features](#geplante-features)
  - [Lizenz](#lizenz)
  - [Kontaktdaten](#kontaktdaten)

## Programme in der Übersicht

- **body_face_hand_trak.py**: Legt eine Maske auf das Gesicht, den Körper und die Hände im Bild (alle drei Masken zusammen).
- **char_full_body_2.py**: Legt eine Maske nur auf den Körper (keine Verwendung des Live Streams, weiße Fläche als Hintergrund).
- **char_trak.py**: Legt Masken auf Gesicht und Hände (Verwendung des Live Streams).
- **char_trak_black.py**: Legt Masken auf Gesicht und Hände (keine Verwendung des Live Streams, schwarze Fläche als Hintergrund).
- **Face_Land_green.py**: Legt eine Maske nur auf das Gesicht (keine Verwendung des Live Streams, schwarze Fläche als Hintergrund, spezielle Merkmale auf Augen und Mund).
- **hand_track_color.py**: Legt Masken auf die Hände im Live Stream (Finger werden in verschiedenen Farben dargestellt).
- **Kamera Testen.py**: Zeigt an, welche Kameras für die Verwendung mit Live Stream und der Bibliothek cv2 angeschlossen sind.
- **mouth_match.py**: Zeigt den Live Stream und zeichnet die Lippenbewegungen in blauer Farbe nach.
- **mouth_match_green.py**: Zeigt einen grünen Hintergrund und die Lippenbewegungen.
- **Nose_image.py**: Zeigt den Live Stream und erfasst die Bewegungen der Nase, auf die ein Bild gelegt wird.
- **Test_face_landmarks.py**: Zeigt den Live Stream und die Gesichtspunkte (Landmarks).
- **Hand_trak_key.py**: Zeigt den Live Stream und verfolgt die Fingerspitzen. Ein virtuelles Keyboard wird dargestellt, auf dem Tasten gedrückt werden, wenn eine Fingerspitze darauf zeigt.
- **char_full_body_4.py**: Zeigt einen schwarzen Hintergrund und legt Masken auf den Körper, die Hände und das Gesicht im Bild.

## Installation

1. **Repository klonen**:
   ```bash
   git clone https://github.com/IhrBenutzername/Virtual_body.git
   cd Virtual_body
   ```

2. **Abhängigkeiten installieren**:
   ```bash
   pip install -r requirements.txt
   ```

## Verwendung

Um eines der Skripte auszuführen, verwenden Sie den folgenden Befehl:
```bash
python <skriptname>.py
```
Beispiel:
```bash
python body_face_hand_trak.py
```

## Projektbeschreibung

Das Projekt Virtual_body nutzt Computer Vision und Maschinelles Lernen, um eine virtuelle Darstellung von Körperteilen und Gesichtszügen zu erstellen. Dies beinhaltet das Auflegen von Masken auf verschiedene Körperteile sowie die Verfolgung und Analyse von Bewegungen in Echtzeit. Das Ziel ist es, eine interaktive und visuell ansprechende Anwendung zu entwickeln, die sowohl für Unterhaltungszwecke als auch für Bildungszwecke genutzt werden kann.

## Geplante Features

- [ ] **README.md aktualisieren**: Hinzufügen von Projektbeschreibung, Kontaktdaten, Lizenz, Anweisungen zur Verwendung.
- [ ] **README.md ins Englische übersetzen**.
- [ ] **Gesichtserkennung**: Bild der Person auf dem Virtual Body anzeigen.
- [ ] **Comic-Transformation**: Gesicht mittels einer API in eine Comicfigur verwandeln und auf dem Virtual Body anzeigen.
- [ ] **Hauptprogramm**: Ein Hauptprogramm erstellen, das alle Funktionen integriert.
- [ ] **Bash-Skript**: Automatisches Starten des Hauptprogramms.
- [ ] **CMD-Skript**: Automatisches Starten des Hauptprogramms auf Windows.

## Lizenz

Dieses Projekt steht unter der [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

## Kontaktdaten

Bei Fragen oder Feedback wenden Sie sich bitte an:
- **Name**: Luna Schätzle
- **Email**: luna.schaetzle@gmail.com
- **GitHub**: [Luna-Schaetzle](www.github.com/Luna-Schaetzle)

