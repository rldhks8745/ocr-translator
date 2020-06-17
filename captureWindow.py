import ctypes
import sys

import cv2
import numpy as np

from PIL import ImageGrab
from PIL.ImageQt import ImageQt
from pytesseract import *

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QCursor, QImage, QPainter, QColor, QPen, QBrush, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QRect

import papagoApi

user32 = ctypes.windll.user32
screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

# window error log
def catch_exceptions(t, val, tb):
    # QMessageBox.critical(None, "An exception was raised", "Exception type: {}".format(t))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

class CaptureWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        captureImage = ImageGrab.grab(bbox=(0, 0, screenWidth, screenHeight))
        self.captureImage = ImageQt(captureImage)

        # cv2.destroyAllWindows()
        # cv2.namedWindow('cvImage')
        # cv2.imshow('cvImage', cv2.cvtColor(np.array(captureImage), cv2.COLOR_BGR2RGB))  # 화면을 보여준다.

        self.sX = 0
        self.sY = 0
        self.eX = 0
        self.eY = 0

        self.drawing = False

        self.translatedText = ""
        self.translatedTextList = None
        self.drawingText = False

        self.initUI()


    def initUI(self):
        self.setWindowTitle('My First Application')

        # 투명 배경색
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 프레임바 제거
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint) # 항상 위에 뜨도록
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.move(0, 0)
        self.resize(screenWidth, screenHeight)
        self.setFocus(True)
        self.activateWindow()
        self.raise_()
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self) # window painter get
        painter.begin(self)

        painter.drawImage(self.rect(), self.captureImage, self.captureImage.rect()) # window painter에 전체 스크린샷찍은 image draw

        if self.sX != 0 and self.sY != 0 and self.eX != 0 and self.eY != 0 :
            painter.setPen(QPen(QColor(255, 0, 0, 255), 1))
            painter.drawRect(self.sX < self.eX and self.sX or self.eX,
                             self.sY < self.eY and self.sY or self.eY,
                             abs(self.eX-self.sX),
                             abs(self.eY-self.sY))

        if self.drawingText:
            fontSize = 15
            margin = 10
            boxHeight = fontSize + (margin * 2)
            boxWidth = fontSize * len(self.translatedTextList[0])

            length = len(self.translatedTextList)
            index = 0

            for text in self.translatedTextList:
                boxWidth = boxWidth < fontSize * len(text) and boxWidth or fontSize * len(text)
            boxWidth = boxWidth * 2
            for text in self.translatedTextList:
                painter.setPen(QColor(255,255,255))
                painter.setBrush(QColor(255, 255, 255))
                painter.drawRect(self.sX,
                                 (self.eY + (boxHeight*length) > screenHeight and self.sY - ((index+1)*boxHeight) or self.eY + (index*boxHeight)),
                                 boxWidth,
                                 fontSize + (margin * 2))

                painter.setPen(QColor(0,0,0))
                painter.setFont(QFont('나눔명조', fontSize))
                painter.drawText(self.sX + margin,
                                 (self.eY + (boxHeight*length) > screenHeight and (self.sY - margin) - (index*boxHeight) or (self.eY  + fontSize + margin) + (index*boxHeight)),
                                 text)
                index = index + 1

        painter.end()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape: # esc 종료
            cv2.destroyAllWindows()
            self.close()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.drawingText = False
            self.sX = e.pos().x()
            self.sY = e.pos().y()
            self.eX = e.pos().x()
            self.eY = e.pos().y()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            self.eX = e.pos().x()
            self.eY = e.pos().y()

            self.update() # paintEvent 호출

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if (self.sX == self.eX) or (self.sY == self.eY) or (abs(self.eX - self.sX) < 10) or (abs(self.eY - self.sY) < 10):
                return

            self.eX = e.pos().x()
            self.eY = e.pos().y()

            # 테두리 1px 빼고 캡처
            cvImage = self.captureImage.copy(self.sX < self.eX and self.sX or self.eX,
                                             self.sY < self.eY and self.sY or self.eY,
                                             abs(self.eX-self.sX),
                                             abs(self.eY-self.sY)).convertToFormat(4)
            cvW = cvImage.width()
            cvH = cvImage.height()
            ptr = cvImage.bits()
            ptr.setsize(cvImage.byteCount())
            arr = np.array(ptr).reshape(cvH, cvW, 4)
            img = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
            cv2.imshow('gray img', img)

            # cv2.destroyAllWindows()
            # cv2.namedWindow('cvImage')
            # cv2.imshow('cvImage', img)  # 화면을 보여준다.

            img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            (thresh, img) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imshow('OTSU img', img)

            out_img = cv2.GaussianBlur(img, (3, 3), 0)
            (thresh, out_img) = cv2.threshold(out_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imshow('cvImage', out_img)

            self.translatedText = image_to_string(out_img, config='--tessdata-dir "tessdata" -l eng --oem 3 --psm 3')
            print("translatedText1: ", self.translatedText)
            self.translatedText = self.translatedText.replace("[^a-zA-Z\s]", "") # 영어, 공백 빼고 다 제거

            if not self.translatedText.strip() == "" :
                # self.translatedText = papagoApi.translate(self.translatedText) # 번역
                #
                self.translatedTextList = self.translatedText.split('\n') # 줄바꿈 split
                # print("translatedText2: ", self.translatedTextList)

                self.drawingText = True
                self.update() # paintEvent 호출
                self.drawing = False
