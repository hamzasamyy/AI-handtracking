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

    total_fingers = 0

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark
            hand_label = results.multi_handedness[hand_no].classification[0].label

            fingers = []

            # Thumb
            if hand_label == "Right":
                if landmarks[tip_ids[0]].x < landmarks[tip_ids[0] - 1].x:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:  # Left hand
                if landmarks[tip_ids[0]].x > landmarks[tip_ids[0] - 1].x:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Other 4 fingers
            for i in range(1, 5):
                if landmarks[tip_ids[i]].y < landmarks[tip_ids[i] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            finger_count = sum(fingers)
            total_fingers += finger_count

            # Wrist position for text
            x = int(landmarks[0].x * image.shape[1])
            y = int(landmarks[0].y * image.shape[0])

            cv2.putText(
                image,
                f"{hand_label}: {finger_count}",
                (x - 30, y - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.putText(
        image,
        f"Total Fingers: {total_fingers}",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("Hand Tracker", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
