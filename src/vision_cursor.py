
import cv2

from .hand_detector import HandDetector, Gesture
from .mouse_controller import MouseController

class VisionCursor:
    def __init__(self):
        # HandDetector
        self.hand_detector = HandDetector()
        self.video = self.hand_detector.video
        self.hands = self.hand_detector.hands

        # MouseController
        self.mouse_controller = MouseController()

        # 클래스 변수
        self.prev_tip_location_x = 0.0
        self.prev_tip_location_y = 0.0

        self.prev_gesture = Gesture.NONE

    def is_cursor_moved(self) -> bool:
        if (self.prev_tip_location_x != self.hand_detector.tip_location_x) and (self.prev_tip_location_y != self.hand_detector.tip_location_y):
            return True
        return False

    def is_clicked(self) -> bool:
        if (self.prev_gesture == Gesture.CLICK) and (self.hand_detector.current_gesture == Gesture.PINCH):
            return True
        return False

    def run(self):
        while self.hand_detector.is_video_opened():
            res = self.hand_detector.process_video()
            if res is False:
                break
            
            if self.is_cursor_moved():
                x_ratio = self.hand_detector.tip_location_x + self.hand_detector.offset_x
                y_ratio = self.hand_detector.tip_location_y + self.hand_detector.offset_y
                self.mouse_controller.move_mouse_to(x_ratio, y_ratio)

            if self.is_clicked():
                print("Mouse Clicked!!")
                self.mouse_controller.mouse_click()

            self.prev_tip_location_x = self.hand_detector.tip_location_x
            self.prev_tip_location_y = self.hand_detector.tip_location_y

            self.prev_gesture = self.hand_detector.current_gesture

        self.video.release()
        cv2.destroyAllWindows()