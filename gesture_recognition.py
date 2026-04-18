import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

tip_ids = [4, 8, 12, 16, 20]

while True:
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks and results.multi_handedness:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark
            hand_label = results.multi_handedness[i].classification[0].label

            fingers = []

            # Thumb open/closed
            if hand_label == "Right":
                thumb_open = landmarks[4].x < landmarks[3].x
            else:
                thumb_open = landmarks[4].x > landmarks[3].x

            fingers.append(1 if thumb_open else 0)

            # Other fingers
            for j in range(1, 5):
                if landmarks[tip_ids[j]].y < landmarks[tip_ids[j] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            finger_count = sum(fingers)

            # Better thumbs up detection
            thumb_tip = landmarks[4]
            thumb_ip = landmarks[3]
            thumb_mcp = landmarks[2]

            thumbs_up = (
                thumb_tip.y < thumb_ip.y < thumb_mcp.y and
                fingers[1] == 0 and
                fingers[2] == 0 and
                fingers[3] == 0 and
                fingers[4] == 0
            )

            peace = (
                fingers[0] == 0 and
                fingers[1] == 1 and
                fingers[2] == 1 and
                fingers[3] == 0 and
                fingers[4] == 0
            )

            open_hand = finger_count == 5

            gesture = "Unknown"
            if thumbs_up:
                gesture = "Thumbs Up"
            elif peace:
                gesture = "Peace"
            elif open_hand:
                gesture = "Open Hand"

            x = int(landmarks[0].x * image.shape[1])
            y = int(landmarks[0].y * image.shape[0])

            cv2.putText(
                image,
                f"{hand_label}: {finger_count}",
                (x - 40, y - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                image,
                gesture,
                (x - 40, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

    cv2.imshow("Hand Tracker", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()