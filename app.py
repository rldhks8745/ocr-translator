import keyboard
import sys
import threading

from PyQt5.QtWidgets import *
from captureWindow import CaptureWindow

def captureImg():
    app = QApplication(sys.argv)
    ex = CaptureWindow()
    ex.show()

    sys.exit(app.exec_())

thread = None

def pressed_keys(e):
    global thread
    for code in keyboard._pressed_events:
        line = ', '.join(str(code))
        print(line, e.name)

    if e.name == "esc":
        if not thread.isAlive():
            print("window thread 삭제")
            thread = None
    elif e.name == "/":
        if thread == None:
            print("window thread 생성")
            thread = threading.Thread(target=captureImg)
            thread.daemon = True
            thread.start()

    print(thread)

keyboard.hook(pressed_keys)
keyboard.wait('0')

# import ctypes
# import cv2
# import keyboard


from PyQt5 import QtCore
from PyQt5.QtCore import Qt
#
# user32 = ctypes.windll.user32
# screenWidth = user32.GetSystemMetrics(0)
# screenHeight = user32.GetSystemMetrics(1)
#
# class MainApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('My First Application')
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
#
#         self.move(0, 0)
#         self.resize(screenWidth, screenHeight)
#         self.show()
#
#     def keyPressEvent(self, e):
#         if e.key() == Qt.Key_Escape:
#             cv2.destroyAllWindows()
#             self.close()
#         # 1번키로 캡쳐뜨기
#         elif e.key() == Qt.Key_1:
#             self.subWindow = CaptureWindow()
#             self.subWindow.show()
#
# def start_capture():
#     print('ctrl+1')
#
# keyboard.add_hotkey("ctrl+1", lambda: start_capture())
#
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = MainApp()
#    ex.show()
#
#    sys.exit(app.exec_())