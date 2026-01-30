from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QMainWindow, QStackedWidget, QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from attendance import add_student, remove_student, clear_attendance, time_in_or_out
from export import export_excel
import re

class ScanWindow(QWidget):
    def __init__(self, go_next, go_next2, go_other):
        super().__init__()
        self.title = QLabel("📋 Attendance System")
        self.subtitle = QLabel("Scan your barcode to time in")
        self.input = QLineEdit()
        self.result = QLabel("Waiting for scan...")
        self.clearAttendance = QPushButton('Clear Attendance')
        self.otherOptions = QPushButton('Other Options')
        self.current_gradelevel = 12
        self.grade11_btn = QPushButton('Grade 11')
        self.grade12_btn = QPushButton('Grade 12')
        self.grade_group = QButtonGroup(self)
        self.grade_group.setExclusive(True)
        self.card = QFrame()
        self.initUI_scan()
        self.go_next = go_next
        self.go_next2 = go_next2
        self.go_other = go_other
        
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

        self.grade_group.addButton(self.grade11_btn, 11)
        self.grade_group.addButton(self.grade12_btn, 12)
        self.grade11_btn.setCheckable(True) 
        self.grade12_btn.setCheckable(True)
        self.grade12_btn.setChecked(True)   
        self.grade_group.buttonClicked[int].connect(self.setGrade)
        self.clearAttendance.clicked.connect(self.on_click_clear)
        self.otherOptions.clicked.connect(self.on_click_other)

        self.card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.grade11_btn)
        top_layout.addWidget(self.grade12_btn)

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(12)
        card_layout.addWidget(self.title)
        card_layout.addWidget(self.subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.input)
        card_layout.addWidget(self.result)
        card_layout.addSpacing(5)
        card_layout.addWidget(self.clearAttendance)
        card_layout.addWidget(self.otherOptions)
        
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
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
            QPushButton {
                background-color: red;
                color: white;
                padding: 5px;
                font-size: 15px    
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)

    def setGrade(self, grade):
        self.current_gradelevel = grade

    def on_click_other(self):
        self.go_other()
    
    def on_click_clear(self, grade):
        self.current_gradelevel = grade
        clear_attendance(int(grade))
        self.result.setText('Attendance cleared!')
        self.result.setStyleSheet('color: green;')

    def scan_id(self):
        student_id = self.input.text().strip()
        grade = self.current_gradelevel

        if not student_id.isdigit():
            self.result.setText("❌ Invalid ID")
            self.result.setStyleSheet("color: red;")
            self.input.clear()
            return

        message = time_in_or_out(int(student_id), int(grade))
        self.result.setText("✅ " + message)
        self.result.setStyleSheet("color: green;")
        self.input.clear()

class addStudent(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.back = QPushButton('Go Back')
        self.title = QLabel('Add a Student')
        self.input_name = QLineEdit()
        self.input_ID = QLineEdit()
        self.input_gradelevel = QLineEdit()
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

        self.input_name.setPlaceholderText('Student Name')
        self.input_name.setAlignment(Qt.AlignCenter)
        self.input_name.setFont(QFont("Segoe UI", 12))
        self.input_name.returnPressed.connect(self.add_student_func)

        self.input_ID.setPlaceholderText("Student ID")
        self.input_ID.setAlignment(Qt.AlignCenter)
        self.input_ID.setFont(QFont("Segoe UI", 12))
        self.input_ID.returnPressed.connect(self.add_student_func)

        self.input_gradelevel.setPlaceholderText("Student Grade Level")
        self.input_gradelevel.setAlignment(Qt.AlignCenter)
        self.input_gradelevel.setFont(QFont("Segoe UI", 12))
        self.input_gradelevel.returnPressed.connect(self.add_student_func)

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
        card_layout.addWidget(self.input_name)
        card_layout.setSpacing(6)
        card_layout.addWidget(self.input_ID)
        card_layout.setSpacing(6)
        card_layout.addWidget(self.input_gradelevel)
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
    @staticmethod
    def is_valid_name(name):
        name = name.strip()
        pattern = r"^[A-Za-z]+([ ,.'-][A-Za-z]+)*\.?$"
        return bool(re.fullmatch(pattern, name))
    #This was supposed to check for valid names but i guess anything can be a valid name lol
    #I will just keep it in for the sake of... Well idk, it looks cool i guess
    
    def add_student_func(self):
        student_id = self.input_ID.text().strip()
        student_name = self.input_name.text().strip()
        student_gradelevel = self.input_gradelevel.text().strip()

        if not student_id.isdigit() and not self.is_valid_name(student_name):
            self.res.setText('❌ Invalid ID and Invalid Student Name')
            self.res.setStyleSheet('color: red;')
            self.input_ID.clear()  
            self.input_name.clear()    
            self.input_gradelevel.clear()      
            return
        elif student_name == '' or student_gradelevel == '' or student_id == '':
            self.res.setText('❌ Invalid Student Name')
            self.res.setStyleSheet('color: red;')
            self.input_name.clear()
            self.input_gradelevel.clear()
        elif not student_id.isdigit() or not student_gradelevel.isdigit():
            self.res.setText('❌ Invalid ID or Grade Level')
            self.res.setStyleSheet('color: red;')
            self.input_ID.clear()  
            self.input_gradelevel.clear()
            return
        else:
            add_student(int(student_id), student_name, int(student_gradelevel))
            self.res.setText('Added student successfully!')
            self.res.setStyleSheet('color: green;')
            self.input_ID.clear()
            self.input_name.clear()
            self.input_gradelevel.clear()

class removeWindow(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.back = QPushButton('Go back')
        self.title = QLabel('Remove Student')
        self.input_ID = QLineEdit()
        self.input_Grade = QLineEdit()
        self.res = QLabel('Waiting...')
        self.card = QFrame()
        self.go_back = go_back
        self.initUI_remove()

    def initUI_remove(self):
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

        self.input_ID.setPlaceholderText('Student ID')
        self.input_ID.setAlignment(Qt.AlignCenter)
        self.input_ID.setFont(QFont("Segoe UI", 12))
        self.input_ID.returnPressed.connect(self.remove_student_func)

        self.input_Grade.setPlaceholderText('Student Grade Level')
        self.input_Grade.setAlignment(Qt.AlignCenter)
        self.input_Grade.setFont(QFont("Segoe UI", 12))
        self.input_Grade.returnPressed.connect(self.remove_student_func)

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
        card_layout.addWidget(self.input_ID)
        card_layout.setSpacing(10)
        card_layout.addWidget(self.input_Grade)
        card_layout.addWidget(self.res)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addStretch()
        layout.addWidget(self.card)
        layout.addStretch()

        self.setLayout(layout)

    def on_click_back(self):
        self.go_back()

    def remove_student_func(self):
        student_id = self.input_ID.text().strip()
        student_gradelevel = self.input_Grade.text().strip()
        if student_id == '' or student_gradelevel == '':
            self.res.setText('❌ Invalid ID or Grade Level')
            self.res.setStyleSheet('color: red;')
            self.input_ID.clear()
            self.input_Grade.clear()
            return
        elif not student_id.isdigit() or not student_gradelevel.isdigit():
            self.res.setText('❌ Invalid ID or Grade Level')
            self.res.setStyleSheet('color: red;')
            self.input_ID.clear()
            self.input_Grade.clear()
            return
        else:
            remove_student(int(student_id), int(student_gradelevel))
            self.res.setText('Succesfully removed student! ')
            self.res.setStyleSheet('color: green;')
            self.input_ID.clear()
            self.input_Grade.clear()

class otherOptions(QWidget):
    def __init__(self, go_back, go_next, go_next2):
        super().__init__()
        self.back = QPushButton('Go back')
        self.title = QLabel('Other Options')
        self.addStudentsbtn = QPushButton('Add a student')
        self.removeStudentbtn = QPushButton('Remove a student')
        self.exportExcel = QPushButton('Export to Excel')
        self.card = QFrame()
        self.go_back = go_back
        self.go_next = go_next
        self.go_next2 = go_next2
        self.initUI_other()

    def initUI_other(self):
        self.addStudentsbtn.clicked.connect(self.on_click_add)
        self.removeStudentbtn.clicked.connect(self.on_click_remove)
        self.exportExcel.clicked.connect(self.on_click_export)  

        self.setStyleSheet("""
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
        card_layout.addWidget(self.addStudentsbtn)
        card_layout.addWidget(self.removeStudentbtn)
        card_layout.addWidget(self.exportExcel)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addStretch()
        layout.addWidget(self.card)
        layout.addStretch()

        self.setLayout(layout)

    def on_click_back(self):
        self.go_back()

    def on_click_add(self):
        self.go_next()

    def on_click_remove(self):
        self.go_next2()

    def on_click_export(self):
        filename = export_excel()
        self.exportExcel.setText(f'Exported to {filename}')
        
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance Scanner")
        self.setGeometry(0, 0, 500, 500)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.ScanWindow = ScanWindow(self.go_next, self.go_next2, self.go_to_other)
        self.addStudent = addStudent(self.go_back)
        self.removeStudent = removeWindow(self.go_back)
        self.goOther = otherOptions(self.go_back, self.go_next, self.go_next2)

        self.stack.addWidget(self.ScanWindow)
        self.stack.addWidget(self.addStudent)
        self.stack.addWidget(self.removeStudent)
        self.stack.addWidget(self.goOther)

    def go_back(self):
        self.stack.setCurrentIndex(0)

    def go_next(self):
        self.stack.setCurrentIndex(1)

    def go_next2(self):
        self.stack.setCurrentIndex(2)
    
    def go_to_other(self):
        self.stack.setCurrentIndex(3)



