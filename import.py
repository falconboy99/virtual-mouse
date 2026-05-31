import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
middle_y = 0  # Track middle finger height

# Click cooldown counter
click_cooldown = 0

# Create a named window and FORCE it to stay on top
cv2.namedWindow('Virtual Mouse', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Virtual Mouse', cv2.WND_PROP_TOPMOST, 1)

# Speed optimization settings
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

while True:
    _, frame = cap.read()
    if frame is None:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if click_cooldown > 0:
        click_cooldown -= 1

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # 1. Index Finger Tracking (Mouse Pointer)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                # 2. Middle Finger Tracking (Scroll Trigger)
                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 255))
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y

                # 3. Thumb Tracking (Action Executer)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Calculate distances
                    click_distance = abs(index_y - thumb_y)
                    scroll_distance = abs(middle_y - thumb_y)

                    # --- SCROLLING LOGIC ---
                    if scroll_distance < 40:
                        if thumb_y < index_y:
                            pyautogui.scroll(120)  # Scroll Up
                        else:
                            pyautogui.scroll(-120)  # Scroll Down

                    # --- CLICKING & MOVING LOGIC ---
                    else:
                        if click_distance < 35:
                            if click_cooldown == 0:
                                pyautogui.click()
                                click_cooldown = 15
                        elif click_distance < 150:
                            pyautogui.moveTo(index_x, index_y)

    cv2.imshow('Virtual Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
