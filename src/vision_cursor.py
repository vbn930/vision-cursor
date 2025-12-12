
import cv2

from .hand_detector import HandDetector
from .mouse_controller import MouseController

class VisionCursor:
    def __init__(self):
        # HandDetector
        self.hand_detector = HandDetector()
        self.video = self.hand_detector.video
        self.hands = self.hand_detector.hands

        # MouseController
        self.mouse_controller = MouseController()
        pass

    def run(self):
        while self.hand_detector.is_video_opened():
            res = self.hand_detector.process_video()
            if res is False:
                break

            x_ratio = self.hand_detector.tip_location_x
            y_ratio = self.hand_detector.tip_location_y
            self.mouse_controller.move_mouse_to(x_ratio, y_ratio)

        self.video.release()
        cv2.destroyAllWindows()