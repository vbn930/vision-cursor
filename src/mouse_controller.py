import pyautogui

class MouseController:
    def __init__(self):
        self.is_dragging = False
        self.width = pyautogui.size().width
        self.height = pyautogui.size().height
        pass

    def move_mouse_to(self, x_ratio: float, y_ratio):
        move_x = int(self.width * x_ratio)
        move_y = int(self.height * y_ratio)

        move_x = max(5, min(move_x, self.width - 5))
        move_y = max(5, min(move_y, self.height - 5))

        pyautogui.moveTo(move_x, move_y)