
import cv2
from hand_detector import HandDetector

class VisionCursor:
    def __init__(self):
        # HandDetector
        self.hand_detector = HandDetector()
        self.video = self.hand_detector.video
        self.hands = self.hand_detector.hands
        pass

    def run(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(img_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    fingers_status = self.hand_detector.get_finger_status(hand_landmarks)
                    print(recognize_gesture(fingers_status))
                    landmark_x, landmark_y = get_tip_location(hand_landmarks, 8)

                    # 손 랜드마크와 연결선 그리기
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # 2. 좌표 변환 공식 (비율 * 해상도)
                    x = int(landmark_x * screen_width)
                    y = int(landmark_y * screen_height)

                    # 3. 마우스 이동
                    pyautogui.moveTo(x, y)

            cv2.imshow('Hand Gesture', frame)
            if cv2.waitKey(1) == 27:  # ESC 키로 종료
                break

        video.release()
        cv2.destroyAllWindows()