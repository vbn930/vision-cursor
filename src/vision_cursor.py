
import cv2

from .hand_detector import HandDetector

class VisionCursor:
    def __init__(self):
        # HandDetector
        self.hand_detector = HandDetector()
        self.video = self.hand_detector.video
        self.hands = self.hand_detector.hands
        pass

    def run(self):
        while self.hand_detector.is_video_opened():
            res = self.hand_detector.process_video()
            if res is False:
                break

        self.video.release()
        cv2.destroyAllWindows()