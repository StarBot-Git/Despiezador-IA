import sys
from PySide6.QtWidgets import QApplication
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(BASE))

from windows.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
