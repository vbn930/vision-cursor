
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
    
    def is_triggered(self, trigger: Gesture, next_gesture: Gesture) -> bool:

        if next_gesture == Gesture.NONE:
            if (self.prev_gesture == trigger) and (self.hand_detector.current_gesture != self.prev_gesture):
                print(f"Triggered by {trigger.name}")
                return True
            return


        if (self.prev_gesture == trigger) and (self.hand_detector.current_gesture == next_gesture):
            print(f"Triggered by {trigger.name}")
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

            if self.is_triggered(Gesture.CLICK, Gesture.PINCH):
                self.mouse_controller.mouse_click()

            if self.is_triggered(Gesture.FIST, Gesture.FIVE):
                self.hand_detector.set_center_offset()
                self.mouse_controller.move_mouse_to(0.5, 0.5)
                pass

            self.prev_tip_location_x = self.hand_detector.tip_location_x
            self.prev_tip_location_y = self.hand_detector.tip_location_y

            self.prev_gesture = self.hand_detector.current_gesture

        self.video.release()
        cv2.destroyAllWindows()