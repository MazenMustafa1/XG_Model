import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QScrollArea, QPushButton)
from Windows import windows




def main():
    app = QApplication(sys.argv)
    main_window = windows.MainWindow()
    # main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()