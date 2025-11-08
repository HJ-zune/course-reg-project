"""
ECE Department Course Registration System - Login Dialog
Handles user authentication
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QGroupBox,
                             QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import Database


class LoginDialog(QDialog):
    """
    Login Dialog for user authentication
    Handles both Student and Admin login
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_info = None
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ECE Course Registration - Login")
        self.setModal(True)
        self.setFixedSize(400, 350)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("ECE Department\nCourse Registration System")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Login form group
        form_group = QGroupBox("Login")
        form_layout = QVBoxLayout()
        
        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(100)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)
        
        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFixedWidth(100)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter your password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Login")
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.handle_login)
        
        self.register_button = QPushButton("Register Student")
        self.register_button.clicked.connect(self.show_register_dialog)
        
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.exit_button)
        
        layout.addLayout(button_layout)
        
        # Info label
        info_label = QLabel("Default Admin: username='admin', password='admin123'")
        info_label.setStyleSheet("color: gray; font-size: 10px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        self.setLayout(layout)
        
        # Connect Enter key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password")
            return
        
        # Authenticate user
        user_info = self.db.authenticate_user(username, password)
        
        if user_info:
            self.user_info = user_info
            QMessageBox.information(self, "Login Successful", 
                                  f"Welcome, {username}!\nRole: {user_info['role']}")
            self.accept()
        else:
            QMessageBox.critical(self, "Login Failed", 
                               "Invalid username or password")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def show_register_dialog(self):
        """Show student registration dialog"""
        register_dialog = StudentRegisterDialog(self)
        if register_dialog.exec():
            QMessageBox.information(self, "Registration Successful", 
                                  "You can now login with your credentials")


class StudentRegisterDialog(QDialog):
    """
    Dialog for new student registration
    Creates both student profile and user account
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Student Registration")
        self.setModal(True)
        self.setFixedSize(450, 500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel("New Student Registration")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Student Information Group
        student_group = QGroupBox("Student Information")
        student_layout = QVBoxLayout()
        
        # Student ID
        sid_layout = QHBoxLayout()
        sid_label = QLabel("Student ID:")
        sid_label.setFixedWidth(120)
        self.sid_input = QLineEdit()
        self.sid_input.setPlaceholderText("e.g., 2021001")
        sid_layout.addWidget(sid_label)
        sid_layout.addWidget(self.sid_input)
        student_layout.addLayout(sid_layout)
        
        # Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Full Name:")
        name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your full name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        student_layout.addLayout(name_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_label.setFixedWidth(120)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("your.email@university.edu")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        student_layout.addLayout(email_layout)
        
        # Program
        program_label = QLabel("Program:")
        student_layout.addWidget(program_label)
        
        self.program_group = QButtonGroup(self)
        programs = ["Computer", "Communications", "Power", "Biomedical"]
        program_layout = QHBoxLayout()
        
        for program in programs:
            radio = QRadioButton(program)
            self.program_group.addButton(radio)
            program_layout.addWidget(radio)
            if program == "Computer":  # Default selection
                radio.setChecked(True)
        
        student_layout.addLayout(program_layout)
        
        # Level
        level_label = QLabel("Current Level:")
        student_layout.addWidget(level_label)
        
        self.level_group = QButtonGroup(self)
        level_layout = QHBoxLayout()
        
        for level in range(1, 5):
            radio = QRadioButton(f"Level {level}")
            self.level_group.addButton(radio, level)
            level_layout.addWidget(radio)
            if level == 1:  # Default selection
                radio.setChecked(True)
        
        student_layout.addLayout(level_layout)
        
        student_group.setLayout(student_layout)
        layout.addWidget(student_group)
        
        # Account Information Group
        account_group = QGroupBox("Account Information")
        account_layout = QVBoxLayout()
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(120)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        account_layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFixedWidth(120)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Choose a password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        account_layout.addLayout(password_layout)
        
        # Confirm Password
        confirm_layout = QHBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setFixedWidth(120)
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setPlaceholderText("Re-enter password")
        confirm_layout.addWidget(confirm_label)
        confirm_layout.addWidget(self.confirm_input)
        account_layout.addLayout(confirm_layout)
        
        account_group.setLayout(account_layout)
        layout.addWidget(account_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.handle_register)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(register_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def handle_register(self):
        """Handle registration"""
        # Validate inputs
        student_id = self.sid_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        # Get selected program
        program = None
        for button in self.program_group.buttons():
            if button.isChecked():
                program = button.text()
                break
        
        # Get selected level
        level = self.level_group.checkedId()
        
        # Validation
        if not all([student_id, name, email, username, password]):
            QMessageBox.warning(self, "Validation Error", 
                              "Please fill in all fields")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Validation Error", 
                              "Passwords do not match")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Validation Error", 
                              "Password must be at least 6 characters")
            return
        
        # Add student to database
        success, message = self.db.add_student(student_id, name, email, program, level)
        
        if not success:
            QMessageBox.critical(self, "Registration Failed", message)
            return
        
        # Get the created student's database ID
        students = self.db.get_all_students()
        student_db_id = None
        for s in students:
            if s['student_id'] == student_id:
                student_db_id = s['id']
                break
        
        # Create user account
        success, message = self.db.register_user(username, password, 'Student', student_db_id)
        
        if not success:
            QMessageBox.critical(self, "Registration Failed", 
                               f"Student created but account failed: {message}")
            return
        
        self.accept()

