import cv2
import mediapipe as mp
import random
import time
import sqlite3
from tkinter import Tk, simpledialog

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# SQLite database file
db_file = 'game_scores.db'

# Keyboard layout definition with non-overlapping and adjusted positions
keyboard_buttons = [
    {'top_left': (50, 30), 'bottom_right': (120, 100), 'color': (255, 0, 0)},
    {'top_left': (180, 30), 'bottom_right': (250, 100), 'color': (0, 255, 0)},
    {'top_left': (310, 30), 'bottom_right': (380, 100), 'color': (0, 0, 255)},
    {'top_left': (50, 150), 'bottom_right': (120, 220), 'color': (255, 255, 0)},
    {'top_left': (180, 150), 'bottom_right': (250, 220), 'color': (255, 0, 255)},
    {'top_left': (310, 150), 'bottom_right': (380, 220), 'color': (0, 255, 255)},
    {'top_left': (50, 270), 'bottom_right': (120, 340), 'color': (192, 192, 192)},
    {'top_left': (180, 270), 'bottom_right': (250, 340), 'color': (128, 128, 128)},
    {'top_left': (310, 270), 'bottom_right': (380, 340), 'color': (64, 64, 64)},
    {'top_left': (440, 30), 'bottom_right': (510, 100), 'color': (128, 0, 0)},
    {'top_left': (440, 150), 'bottom_right': (510, 220), 'color': (0, 128, 0)},
    {'top_left': (440, 270), 'bottom_right': (510, 340), 'color': (0, 0, 128)}
]

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to check if a point is inside a rectangle
def is_over_button(point, button):
    x, y = point
    if button['top_left'][0] < x < button['bottom_right'][0] and button['top_left'][1] < y < button['bottom_right'][1]:
        return True
    return False

# Function to get a random button index
def get_random_button_index():
    return random.randint(0, len(keyboard_buttons) - 1)

# Function to draw buttons with labels
def draw_button(image, button):
    cv2.rectangle(image, button['top_left'], button['bottom_right'], button['color'], cv2.FILLED)
    cv2.putText(image, button['label'], (button['top_left'][0] + 10, button['top_left'][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Function to save the score to the database
def save_score_to_db(name, score):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as err:
        print(f"Error: {err}")

# Function to get the top 5 scores from the database
def get_top_scores():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 3")
        top_scores = cursor.fetchall()
        cursor.close()
        conn.close()
        return top_scores
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return []

def main():
    initialize_db()
    cap = cv2.VideoCapture(0)
    last_score = 0
    player_name = ""

    with mp_hands.Hands(model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        while True:
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Mirror the image horizontally for a selfie-view display
            image = cv2.flip(image, 1)

            # Get image dimensions
            image_height, image_width, _ = image.shape
            control_buttons = {
                'start': {'top_left': (image_width//2 - 100, image_height//2 - 60), 'bottom_right': (image_width//2 + 100, image_height//2 - 10), 'color': (0, 255, 0), 'label': 'Start Game'},
            }

            # Convert the BGR image to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Convert back to BGR for OpenCV
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw control buttons
            for button in control_buttons.values():
                draw_button(image, button)

            # Display the last score
            cv2.putText(image, f"Last Score: {last_score}", (image.shape[1] - 300, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the top 5 scores
            top_scores = get_top_scores()
            cv2.putText(image, "High Scores:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            for i, (name, score) in enumerate(top_scores):
                cv2.putText(image, f"{i + 1}. {name}: {score}", (50, 100 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get the tip of the index finger
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    index_tip_x, index_tip_y = int(index_finger_tip.x * image.shape[1]), int(index_finger_tip.y * image.shape[0])

                    # Check if the index finger tip is over the start button
                    if is_over_button((index_tip_x, index_tip_y), control_buttons['start']):
                        Tk().withdraw()  # Hide the main window
                        player_name = simpledialog.askstring("Input", "What is your name?")
                        last_score = game_loop(cap, hands)
                        save_score_to_db(player_name, last_score)
                        break

            

            # Display the resulting image
            cv2.imshow('MediaPipe Hands Game', image)

            # Check for exit
            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

def game_loop(cap, hands):
    current_target_index = get_random_button_index()
    score = 0
    time_limit = 10  # Set the time limit for the game
    end_time = time.time() + time_limit

    while True:
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Mirror the image horizontally for a selfie-view display
        image = cv2.flip(image, 1)

        # Convert the BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Convert back to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw the keyboard buttons
        for button in keyboard_buttons:
            cv2.rectangle(image, button['top_left'], button['bottom_right'], button['color'], cv2.FILLED)

        # Display the current target color at the bottom
        target_color = keyboard_buttons[current_target_index]['color']
        cv2.putText(image, f"Touch this color:", (50, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.rectangle(image, (400, image.shape[0] - 100), (500, image.shape[0] - 50), target_color, cv2.FILLED)

        # Calculate and display the remaining time in the top right corner
        remaining_time = int(end_time - time.time())
        cv2.putText(image, f"Time: {remaining_time}s", (image.shape[1] - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the score in the bottom right corner
        cv2.putText(image, f"Score: {score}", (image.shape[1] - 150, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Process hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the tip of the index finger
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_tip_x, index_tip_y = int(index_finger_tip.x * image.shape[1]), int(index_finger_tip.y * image.shape[0])

                # Check if the index finger tip is over the target button
                if is_over_button((index_tip_x, index_tip_y), keyboard_buttons[current_target_index]):
                    score += 1
                    current_target_index = get_random_button_index()

        # Display the resulting image
        cv2.imshow('MediaPipe Hands Game', image)

        # Check for exit
        if cv2.waitKey(5) & 0xFF == 27:
            break

        # Check for time limit
        if remaining_time <= 0:
            break

    return score

if __name__ == '__main__':
    main()
