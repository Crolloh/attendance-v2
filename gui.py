from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from attendance import record_attendance, add_student

class ScanWindow(QWidget):
    def __init__(self, go_next):
        super().__init__()
        self.title = QLabel("📋 Attendance System")
        self.subtitle = QLabel("Scan your barcode to time in")
        self.input = QLineEdit()
        self.result = QLabel("Waiting for scan...")
        self.addStudentsbtn = QPushButton('Add a student')
        self.card = QFrame()
        self.initUI_scan()
        self.go_next = go_next
        
    def initUI_scan(self):
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("color: gray;")

        self.input.setPlaceholderText("Student ID")
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setFont(QFont("Segoe UI", 12))
        self.input.returnPressed.connect(self.scan_id)

        self.result.setAlignment(Qt.AlignCenter)

        self.addStudentsbtn.setStyleSheet('background-color: red;'
                                          'color: white;'
                                          'padding: 5px;'
                                          'font-size: 15px')
        self.addStudentsbtn.clicked.connect(self.on_click_next)

        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(12)
        card_layout.addWidget(self.title)
        card_layout.addWidget(self.subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.input)
        card_layout.addWidget(self.result)
        card_layout.addWidget(self.addStudentsbtn)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.card)
        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget { background: #f2f4f8; }
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
    def on_click_next(self):
        self.go_next()

    def scan_id(self):
        student_id = self.input.text().strip()

        if not student_id.isdigit():
            self.result.setText("❌ Invalid ID")
            self.result.setStyleSheet("color: red;")
            self.input.clear()
            return

        message = record_attendance(int(student_id))
        self.result.setText("✅ " + message)
        self.result.setStyleSheet("color: green;")
        self.input.clear()

class addStudent(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.back = QPushButton('Go Back')
        self.title = QLabel('Add a Student')
        self.input = QLineEdit()
        self.res = QLabel('Waiting for scan...')
        self.card = QFrame()
        self.initUI_add()
        self.go_back = go_back

    def initUI_add(self):

        self.back.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #357ABD;     
            }  
        """)
        self.back.clicked.connect(self.on_click_back)

        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.input.setPlaceholderText("Student ID")
        self.input.setAlignment(Qt.AlignCenter)
        self.input.setFont(QFont("Segoe UI", 12))

        self.res.setAlignment(Qt.AlignCenter)

        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 20px;
            }       
        """)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back)
        top_layout.addStretch()

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(14)
        card_layout.addWidget(self.title)
        card_layout.setSpacing(10)
        card_layout.addWidget(self.input)
        card_layout.setSpacing(10)
        card_layout.addWidget(self.res)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addStretch()
        layout.addWidget(self.card)
        layout.addStretch()

        self.setLayout(layout)

    def on_click_back(self):
        self.go_back()

    def addStudent(self):
        student_id = self.input.text().strip()

        if not student_id.isdigit():
            self.res.setText('❌ Invalid ID')
            self.res.setStyleSheet('color: red;')
            self.input.clear()            
            return
        
        add_student(int(student_id))
        self.res.setText('Added student successfully!')
        self.res.setStyleSheet('color: green;')
        self.input.clear()
        



class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Scanner")
        self.setGeometry(0, 0, 500, 500)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.ScanWindow = ScanWindow(self.go_next)
        self.addStudent = addStudent(self.go_back)

        self.stack.addWidget(self.ScanWindow)
        self.stack.addWidget(self.addStudent)

    def go_next(self):
        self.stack.setCurrentIndex(1)

    def go_back(self):
        self.stack.setCurrentIndex(0)



