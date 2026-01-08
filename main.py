#startup 
import sys
from PyQt5.QtWidgets import QApplication
from gui import AttendanceUI
from attendance import init_db

if __name__ == "__main__":
    init_db()  

    app = QApplication(sys.argv)
    window = AttendanceUI()
    window.show()
    sys.exit(app.exec_())
