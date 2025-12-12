from enum import Enum, auto
from collections import Counter

import cv2
import mediapipe as mp

class Gesture(Enum):
    ONE = auto(),
    TWO = auto(),
    THREE = auto(),
    FOUR = auto(),
    FIVE = auto(),
    PINCH = auto(),
    NONE = auto()


class HandDetector:
    def __init__(self):
        # 클래스 변수
        self.gesture_queue = list(Gesture) # 5개 프레임에서 연속적으로 제스처가 인식 되어야 인정
        self.gesture_queue = [Gesture.NONE] * 5

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
            fingers.append(True)
        else:
            fingers.append(False)

        # 나머지 손가락: 각 손가락의 팁 (8, 12, 16, 20)이 PIP (6, 10, 14, 18) 위에 있으면 펼쳐진 상태
        tips = [8, 12, 16, 20]
        pip_joints = [6, 10, 14, 18]
        for tip, pip in zip(tips, pip_joints):
            if hand.landmark[tip].y < hand.landmark[pip].y:
                fingers.append(True) # 굽은 상태
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

        gesture_list = [one, two, three, four, five, pinch]

        for i in range(len(gesture_list)):
            if fingers is gesture_list[i]:
                return Gesture(i + 1)
        
        return Gesture.NONE
    
    def get_current_gesture(self) -> Gesture:
        counts = Counter(self.gesture_queue)
        most_frequent = counts.most_common(1)
        print(most_frequent)
        val, count = most_frequent[0]

        if count is 5:
            return val
        else:
            return Gesture.NONE
        
    def process_video(self):
        pass
