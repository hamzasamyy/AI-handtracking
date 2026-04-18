import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

def dist(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

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

            lm = hand_landmarks.landmark
            hand_label = results.multi_handedness[i].classification[0].label
            wrist = lm[0]

            # Gesture logic
            thumb_extended = dist(lm[4], wrist) > dist(lm[3], wrist)
            index_extended = dist(lm[8], wrist) > dist(lm[6], wrist)
            middle_extended = dist(lm[12], wrist) > dist(lm[10], wrist)
            ring_extended = dist(lm[16], wrist) > dist(lm[14], wrist)
            pinky_extended = dist(lm[20], wrist) > dist(lm[18], wrist)

            gesture = "Unknown"

            if (
                index_extended and middle_extended and
                not ring_extended and not pinky_extended
            ):
                gesture = "Peace ✌️"

            elif all([
                thumb_extended,
                index_extended,
                middle_extended,
                ring_extended,
                pinky_extended
            ]):
                gesture = "Open Hand ✋"

            elif (
                thumb_extended and
                not index_extended and
                not middle_extended and
                not ring_extended and
                not pinky_extended and
                lm[4].y < lm[0].y
            ):
                gesture = "Thumbs Up 👍"

            x = int(lm[0].x * image.shape[1])
            y = int(lm[0].y * image.shape[0])

            cv2.putText(
                image,
                hand_label,
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