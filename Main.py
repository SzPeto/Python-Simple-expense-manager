import sys

from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

class Main:
    def __init__(self):
        app = QApplication(sys.argv)
        window = MainWindow(self)
        window.show()
        sys.exit(app.exec_())

def main():
    Main()

if __name__ == "__main__":
    main()