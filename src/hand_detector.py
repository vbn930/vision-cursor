from enum import Enum, auto
from collections import Counter

import cv2
import mediapipe as mp

class Gesture(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    PINCH = 6
    NONE = 7


class HandDetector:
    def __init__(self):
        # 클래스 변수
        self.consecutive_num = 1
        self.gesture_queue = list(Gesture) # 5개 프레임에서 연속적으로 제스처가 인식 되어야 인정
        self.gesture_queue = [Gesture.NONE] * self.consecutive_num
        self.tip_location_x = 0
        self.tip_location_y = 0

        # Mediapipe 설정
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

        # Opencv
        self.camera_num = 0
        self.video = cv2.VideoCapture(self.camera_num)
        pass
    
    def get_finger_status(self, hand) -> list:
        """
        손가락이 펴져 있는지 접혀 있는지 확인하는 함수
        """
        # 오른손만 사용
        fingers = []

        # 엄지: 랜드마크 4가 랜드마크 2의 오른쪽에 있으면 펼쳐진 상태
        if hand.landmark[4].x < hand.landmark[3].x:
            fingers.append(False)
        else:
            fingers.append(True)

        # 나머지 손가락: 각 손가락의 팁 (8, 12, 16, 20)이 PIP (6, 10, 14, 18) 위에 있으면 펼쳐진 상태
        tips = [8, 12, 16, 20]
        pip_joints = [5, 9, 13, 17]
        for tip, pip in zip(tips, pip_joints):
            if hand.landmark[tip].y < hand.landmark[pip].y:
                fingers.append(False) # 굽은 상태
            else:
                fingers.append(True) # 펼쳐진 상태

        return fingers

    def add_gesture(self, new_gesture: Gesture):
        self.gesture_queue.pop(0)
        self.gesture_queue.append(new_gesture)

    def get_frame_gesture(self, fingers: list) -> Gesture:
        one = [True, False, True, True, True] # 검지만 펴져 있는 상태
        two = [True, False, False, True, True] # 검지, 중지 펴져 있는 상태
        three = [False, False, False, True, True] # 엄지, 검지, 중지 펴져 있는 상태
        four = [True, False, False, False, False] # 검지, 중지, 약지, 소지 펴져 있는 상태
        five = [False, False, False, False, False] # 모든 손가락 펴져 있는 상태
        pinch = [False, False, True, True, True] # 엄지, 검지 펴져 있는 상태

        if fingers == one:
            return Gesture.ONE
        
        if fingers == two:
            return Gesture.TWO
        
        if fingers == three:
            return Gesture.THREE
        
        if fingers == four:
            return Gesture.FOUR
        
        if fingers == five:
            return Gesture.FIVE
        
        if fingers == pinch:
            return Gesture.PINCH
        
        return Gesture.NONE
    
    def get_current_gesture(self) -> Gesture:
        counts = Counter(self.gesture_queue)
        most_frequent = counts.most_common(1)
        val, count = most_frequent[0]

        if count == self.consecutive_num:
            return val
        else:
            return Gesture.NONE
        
    def get_landmark_position(self, hands, landmark_num):
        return hands.landmark[landmark_num].x, hands.landmark[landmark_num].y
        
    def process_video(self) -> bool:
        ret, frame = self.video.read()
        if not ret:
            return False

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(img_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                fingers_status = self.get_finger_status(hand_landmarks)
                gesture = self.get_frame_gesture(fingers_status)
                self.add_gesture(gesture)

                if (gesture == Gesture.ONE) or (gesture == Gesture.PINCH):
                    self.tip_location_x, self.tip_location_y = self.get_landmark_position(hand_landmarks, 8)

                # 손 랜드마크와 연결선 그리기
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        current_gesture = self.get_current_gesture()
        print(f"Current Gesture: {current_gesture.name}, Tip pos: ({self.tip_location_y}, {self.tip_location_x})")
        cv2.imshow('Hand Gesture', frame)
        if cv2.waitKey(1) == 27:  # ESC 키로 종료
            return False

        return True

    def is_video_opened(self) -> bool:
        return self.video.isOpened()
