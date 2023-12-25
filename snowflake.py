import sys
import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from PyQt5.QtGui import QPainter, QPixmap


class SnowFall(QFrame):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.snowflakePixmap = QPixmap('snowflake.png')
        self.initUI()

    def initUI(self) -> None:
        self.snowflakes = []
        self.timer = QTimer(self)

        self.timer.timeout.connect(self.updateSnowflakes)
        self.timer.start(16)

        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.setWindowTitle('Snow Fall')

    def paintEvent(self, event) -> None:
        qp = QPainter()
        qp.begin(self)
        self.drawSnowflakes(qp)
        qp.end()

    def drawSnowflakes(self, qp: QPainter) -> None:
        for x, y, size, _ in self.snowflakes:
            scaledPixmap = self.snowflakePixmap.scaled(size, size)
            qp.drawPixmap(int(x), int(y), scaledPixmap)

    def updateSnowflakes(self) -> None:
        elapsed = self.elapsedTimer.elapsed()
        self.elapsedTimer.restart()

        dt = elapsed / 1000.0

        if random.choice([True, False]):
            x, y = random.randint(0, self.width()), 0
            speed = 200
            size = random.randint(20, 40)

            self.snowflakes.append((x, y, size, speed))

        new_snowflakes = []
        for x, y, size, speed in self.snowflakes:
            y += speed * dt
            if y < self.height():
                new_snowflakes.append((x, y, size, speed))

        self.snowflakes = new_snowflakes
        self.update()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.frame = SnowFall(self)
        self.setCentralWidget(self.frame)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showFullScreen()
    sys.exit(app.exec_())