from concurrent.futures import thread
from time import strptime
from tkinter import Frame
import cv2
import sys
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot,QRect
from PyQt5.QtGui import QImage, QPixmap,QTransform
from datetime import datetime
import os
from PIL import Image
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive=True
        cap = cv2.VideoCapture(0)
        self.logic=1
        self.count=0
        while self.ThreadActive:
            
            ret, frame = cap.read()
            if ret:
                cv2.waitKey()
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if self.logic==2:
                    cv2.imwrite("son" + ".png", frame)
                    cv2.imwrite(str(self.count) + ".png", frame)
                    self.count+=1
                    self.logic=1
    def stop(self):
        self.ThreadActive=False
        self.quit()
    

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setStyleSheet("background-color: rgb(132, 61, 255);")
        self.setWindowTitle("Demo")
        self.resize(1800, 1200)
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QRect(490, 40, 621, 101))
        self.stopBtn = QPushButton(self.groupBox)
        self.stopBtn.setGeometry(QRect(10, 20, 191, 61))
        self.stopBtn.setText("CLOSE")
        self.stopBtn.setStyleSheet("background-color: rgb(170, 255, 255)")
        self.takePhotoBtn = QPushButton(self.groupBox)
        self.takePhotoBtn.setGeometry(QRect(210, 20, 191, 61))
        self.takePhotoBtn.setStyleSheet("background-color : rgb(170, 255, 255)")
        self.takePhotoBtn.setText("TAKE PHOTO")
        self.showPhotoBtn = QPushButton(self.groupBox)
        self.showPhotoBtn.setGeometry(QRect(420, 20, 190, 61))
        self.showPhotoBtn.setStyleSheet("background-color: rgb(170, 255, 255)")
        self.showPhotoBtn.setText("SHOW PHOTO")
        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setGeometry(QRect(940, 150, 741, 651))
        self.groupBox_2.setStyleSheet("border-color: rgb(142, 255, 66);")
        self.label2 = QLabel(self.groupBox_2)
        self.label2.setGeometry(QRect(50, 40, 640, 480))
        self.zoomInBtn = QPushButton(self.groupBox_2)
        self.zoomInBtn.setGeometry(QRect(240, 550, 171, 51))
        self.zoomInBtn.setStyleSheet("background-color: rgb(142, 255, 66);")
        self.zoomInBtn.setText("ZOOM IN")
        self.zoomOutBtn = QPushButton(self.groupBox_2)
        self.zoomOutBtn.setGeometry(QRect(450, 550, 171, 51))
        self.zoomOutBtn.setStyleSheet("background-color: rgb(142, 255, 66);")
        self.zoomOutBtn.setText("ZOOM OUT")
        self.groupBox_3 = QGroupBox(self)
        self.groupBox_3.setGeometry(QRect(30, 150, 771, 651))
        self.groupBox_3.setStyleSheet("border-color: rgb(142, 255, 66);")
        self.label = QLabel(self.groupBox_3)
        self.label.setGeometry(QRect(60, 40, 640, 480))
        self.stopBtn.clicked.connect(self.cancel)
        self.zoomInBtn.clicked.connect(self.zoom_in)
        self.zoomOutBtn.clicked.connect(self.zoom_out)
        self.showPhotoBtn.clicked.connect(self.showImage)
        self.takePhotoBtn.clicked.connect(self.takePhoto)
        self.th = Thread()
        self.scale = 1
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.show()
    def cancel(self):
        cv2.destroyAllWindows()
    def takePhoto(self):
        self.th.logic=2
    def showImage(self):
        print("show")
        self.ThreadActive=False
        self.im = QPixmap("son.png")
        self.label2.setPixmap(self.im)
    def zoom_in(self):
        self.scale *= 2
        self.resize_image()
    def zoom_out(self):
        self.scale /= 2
        self.resize_image()
    def resize_image(self):
        size = self.im.size()
        scaled_pixmap = self.im.scaled(self.scale * size)
        self.label2.setPixmap(scaled_pixmap)
        self.label2.setFixedSize(640, 480)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())