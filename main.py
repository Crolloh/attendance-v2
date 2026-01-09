#startup 
import sys
from PyQt5.QtWidgets import QApplication
from gui import mainWindow
from attendance import init_db

if __name__ == "__main__":
    init_db()  

    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())
