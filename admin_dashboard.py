"""
ECE Department Course Registration System - Admin Dashboard
Provides admin interface for course and curriculum management
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTabWidget, QTableWidget, QTableWidgetItem, QLineEdit,
                             QTextEdit, QSpinBox, QComboBox, QMessageBox, QGroupBox,
                             QHeaderView, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import Database
from models import Course


class AdminDashboard(QWidget):
    """
    Admin Dashboard
    Central interface for administrators to manage the system
    """
    
    def __init__(self, main_window, user_info):
        super().__init__()
        self.main_window = main_window
        self.user_info = user_info
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Admin Dashboard")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.main_window.logout)
        header_layout.addWidget(logout_button)
        
        layout.addLayout(header_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_courses_tab(), "Courses")
        self.tabs.addTab(self.create_students_tab(), "Students")
        self.tabs.addTab(self.create_program_plan_tab(), "Program Plans")
        self.tabs.addTab(self.create_schedules_tab(), "Course Schedules")
        self.tabs.addTab(self.create_registrations_tab(), "Registrations")
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def create_courses_tab(self):
        """Create courses management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Add course form
        form_group = QGroupBox("Add New Course")
        form_layout = QVBoxLayout()
        
        # Row 1: Code and Name
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Course Code:"))
        self.course_code_input = QLineEdit()
        self.course_code_input.setPlaceholderText("e.g., COE310")
        row1.addWidget(self.course_code_input)
        
        row1.addWidget(QLabel("Course Name:"))
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("e.g., Data Structures")
        row1.addWidget(self.course_name_input, 2)
        form_layout.addLayout(row1)
        
        # Row 2: Credits, Lecture, Lab, Capacity
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Credits:"))
        self.credits_input = QSpinBox()
        self.credits_input.setRange(1, 6)
        self.credits_input.setValue(3)
        row2.addWidget(self.credits_input)
        
        row2.addWidget(QLabel("Lecture Hours:"))
        self.lecture_hours_input = QSpinBox()
        self.lecture_hours_input.setRange(0, 10)
        self.lecture_hours_input.setValue(3)
        row2.addWidget(self.lecture_hours_input)
        
        row2.addWidget(QLabel("Lab Hours:"))
        self.lab_hours_input = QSpinBox()
        self.lab_hours_input.setRange(0, 10)
        self.lab_hours_input.setValue(0)
        row2.addWidget(self.lab_hours_input)
        
        row2.addWidget(QLabel("Max Capacity:"))
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(10, 200)
        self.capacity_input.setValue(30)
        row2.addWidget(self.capacity_input)
        form_layout.addLayout(row2)
        
        # Row 3: Description
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Description:"))
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Brief course description")
        row3.addWidget(self.description_input, 3)
        form_layout.addLayout(row3)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_course_btn = QPushButton("Add Course")
        add_course_btn.clicked.connect(self.add_course)
        button_layout.addWidget(add_course_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_courses)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        form_layout.addLayout(button_layout)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Courses table
        self.courses_table = QTableWidget()
        self.courses_table.setColumnCount(7)
        self.courses_table.setHorizontalHeaderLabels([
            "ID", "Code", "Name", "Credits", "Lec Hours", "Lab Hours", "Capacity"
        ])
        self.courses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.courses_table)
        
        tab.setLayout(layout)
        self.refresh_courses()
        return tab
    
    def create_students_tab(self):
        """Create students management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Search and filters
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.student_search_input = QLineEdit()
        self.student_search_input.setPlaceholderText("Search by ID or name")
        search_layout.addWidget(self.student_search_input)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.refresh_students)
        search_layout.addWidget(search_btn)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_students)
        search_layout.addWidget(refresh_btn)
        
        layout.addLayout(search_layout)
        
        # Students table
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(6)
        self.students_table.setHorizontalHeaderLabels([
            "DB ID", "Student ID", "Name", "Email", "Program", "Level"
        ])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.students_table)
        
        tab.setLayout(layout)
        self.refresh_students()
        return tab
    
    def create_program_plan_tab(self):
        """Create program plans management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Add to program plan form
        form_group = QGroupBox("Add Course to Program Plan")
        form_layout = QVBoxLayout()
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Program:"))
        self.plan_program_combo = QComboBox()
        self.plan_program_combo.addItems(["Computer", "Communications", "Power", "Biomedical"])
        row1.addWidget(self.plan_program_combo)
        
        row1.addWidget(QLabel("Level:"))
        self.plan_level_spin = QSpinBox()
        self.plan_level_spin.setRange(1, 4)
        self.plan_level_spin.setValue(1)
        row1.addWidget(self.plan_level_spin)
        
        row1.addWidget(QLabel("Semester:"))
        self.plan_semester_spin = QSpinBox()
        self.plan_semester_spin.setRange(1, 2)
        self.plan_semester_spin.setValue(1)
        row1.addWidget(self.plan_semester_spin)
        form_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Course Code:"))
        self.plan_course_input = QLineEdit()
        self.plan_course_input.setPlaceholderText("e.g., COE310")
        row2.addWidget(self.plan_course_input)
        
        self.plan_elective_check = QCheckBox("Elective")
        row2.addWidget(self.plan_elective_check)
        
        add_plan_btn = QPushButton("Add to Plan")
        add_plan_btn.clicked.connect(self.add_to_program_plan)
        row2.addWidget(add_plan_btn)
        form_layout.addLayout(row2)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Add prerequisite form
        prereq_group = QGroupBox("Add Prerequisite")
        prereq_layout = QHBoxLayout()
        
        prereq_layout.addWidget(QLabel("Course:"))
        self.prereq_course_input = QLineEdit()
        self.prereq_course_input.setPlaceholderText("e.g., COE310")
        prereq_layout.addWidget(self.prereq_course_input)
        
        prereq_layout.addWidget(QLabel("Requires:"))
        self.prereq_required_input = QLineEdit()
        self.prereq_required_input.setPlaceholderText("e.g., COE200")
        prereq_layout.addWidget(self.prereq_required_input)
        
        add_prereq_btn = QPushButton("Add Prerequisite")
        add_prereq_btn.clicked.connect(self.add_prerequisite)
        prereq_layout.addWidget(add_prereq_btn)
        
        prereq_group.setLayout(prereq_layout)
        layout.addWidget(prereq_group)
        
        # View program plan
        view_layout = QHBoxLayout()
        view_layout.addWidget(QLabel("View Plan for:"))
        self.view_program_combo = QComboBox()
        self.view_program_combo.addItems(["Computer", "Communications", "Power", "Biomedical"])
        view_layout.addWidget(self.view_program_combo)
        
        self.view_level_spin = QSpinBox()
        self.view_level_spin.setRange(1, 4)
        view_layout.addWidget(self.view_level_spin)
        
        self.view_semester_spin = QSpinBox()
        self.view_semester_spin.setRange(1, 2)
        view_layout.addWidget(self.view_semester_spin)
        
        view_btn = QPushButton("View Plan")
        view_btn.clicked.connect(self.view_program_plan)
        view_layout.addWidget(view_btn)
        view_layout.addStretch()
        
        layout.addLayout(view_layout)
        
        # Program plan table
        self.program_plan_table = QTableWidget()
        self.program_plan_table.setColumnCount(6)
        self.program_plan_table.setHorizontalHeaderLabels([
            "Course Code", "Name", "Credits", "Lecture", "Lab", "Elective"
        ])
        self.program_plan_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.program_plan_table)
        
        tab.setLayout(layout)
        return tab
    
    def create_schedules_tab(self):
        """Create course schedules management tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Add schedule form
        form_group = QGroupBox("Add Course Schedule")
        form_layout = QVBoxLayout()
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Course Code:"))
        self.sched_course_input = QLineEdit()
        self.sched_course_input.setPlaceholderText("e.g., COE310")
        row1.addWidget(self.sched_course_input)
        
        row1.addWidget(QLabel("Semester:"))
        self.sched_semester_input = QLineEdit()
        self.sched_semester_input.setPlaceholderText("e.g., Fall 2025")
        row1.addWidget(self.sched_semester_input)
        form_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Day:"))
        self.sched_day_combo = QComboBox()
        self.sched_day_combo.addItems(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"])
        row2.addWidget(self.sched_day_combo)
        
        row2.addWidget(QLabel("Start:"))
        self.sched_start_input = QLineEdit()
        self.sched_start_input.setPlaceholderText("08:00")
        row2.addWidget(self.sched_start_input)
        
        row2.addWidget(QLabel("End:"))
        self.sched_end_input = QLineEdit()
        self.sched_end_input.setPlaceholderText("10:00")
        row2.addWidget(self.sched_end_input)
        
        row2.addWidget(QLabel("Room:"))
        self.sched_room_input = QLineEdit()
        self.sched_room_input.setPlaceholderText("A101")
        row2.addWidget(self.sched_room_input)
        
        self.sched_is_lab_check = QCheckBox("Is Lab")
        row2.addWidget(self.sched_is_lab_check)
        
        form_layout.addLayout(row2)
        
        add_sched_btn = QPushButton("Add Schedule")
        add_sched_btn.clicked.connect(self.add_course_schedule)
        form_layout.addWidget(add_sched_btn)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        layout.addWidget(QLabel("Schedule management interface"))
        
        tab.setLayout(layout)
        return tab
    
    def create_registrations_tab(self):
        """Create registrations overview tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Semester:"))
        self.reg_semester_input = QLineEdit()
        self.reg_semester_input.setPlaceholderText("e.g., Fall 2025")
        filter_layout.addWidget(self.reg_semester_input)
        
        view_regs_btn = QPushButton("View Registrations")
        view_regs_btn.clicked.connect(self.view_registrations)
        filter_layout.addWidget(view_regs_btn)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # Registrations table
        self.registrations_table = QTableWidget()
        self.registrations_table.setColumnCount(6)
        self.registrations_table.setHorizontalHeaderLabels([
            "Student ID", "Student Name", "Course Code", "Course Name", "Semester", "Status"
        ])
        self.registrations_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.registrations_table)
        
        tab.setLayout(layout)
        return tab
    
    # Action methods
    def add_course(self):
        """Add a new course"""
        code = self.course_code_input.text().strip()
        name = self.course_name_input.text().strip()
        credits = self.credits_input.value()
        lec_hours = self.lecture_hours_input.value()
        lab_hours = self.lab_hours_input.value()
        capacity = self.capacity_input.value()
        desc = self.description_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "Validation Error", "Course code and name are required")
            return
        
        success, message = self.db.add_course(code, name, credits, lec_hours, lab_hours, capacity, desc)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_course_form()
            self.refresh_courses()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def clear_course_form(self):
        """Clear course input form"""
        self.course_code_input.clear()
        self.course_name_input.clear()
        self.description_input.clear()
        self.credits_input.setValue(3)
        self.lecture_hours_input.setValue(3)
        self.lab_hours_input.setValue(0)
        self.capacity_input.setValue(30)
    
    def refresh_courses(self):
        """Refresh courses table"""
        courses = self.db.get_all_courses()
        self.courses_table.setRowCount(len(courses))
        
        for i, course in enumerate(courses):
            self.courses_table.setItem(i, 0, QTableWidgetItem(str(course['id'])))
            self.courses_table.setItem(i, 1, QTableWidgetItem(course['course_code']))
            self.courses_table.setItem(i, 2, QTableWidgetItem(course['name']))
            self.courses_table.setItem(i, 3, QTableWidgetItem(str(course['credits'])))
            self.courses_table.setItem(i, 4, QTableWidgetItem(str(course['lecture_hours'])))
            self.courses_table.setItem(i, 5, QTableWidgetItem(str(course['lab_hours'])))
            self.courses_table.setItem(i, 6, QTableWidgetItem(str(course['max_capacity'])))
    
    def refresh_students(self):
        """Refresh students table"""
        students = self.db.get_all_students()
        self.students_table.setRowCount(len(students))
        
        for i, student in enumerate(students):
            self.students_table.setItem(i, 0, QTableWidgetItem(str(student['id'])))
            self.students_table.setItem(i, 1, QTableWidgetItem(student['student_id']))
            self.students_table.setItem(i, 2, QTableWidgetItem(student['name']))
            self.students_table.setItem(i, 3, QTableWidgetItem(student['email']))
            self.students_table.setItem(i, 4, QTableWidgetItem(student['program']))
            self.students_table.setItem(i, 5, QTableWidgetItem(str(student['level'])))
    
    def add_to_program_plan(self):
        """Add course to program plan"""
        program = self.plan_program_combo.currentText()
        level = self.plan_level_spin.value()
        semester = self.plan_semester_spin.value()
        course_code = self.plan_course_input.text().strip()
        is_elective = self.plan_elective_check.isChecked()
        
        if not course_code:
            QMessageBox.warning(self, "Validation Error", "Course code is required")
            return
        
        success, message = self.db.add_to_program_plan(program, level, semester, course_code, is_elective)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.plan_course_input.clear()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def add_prerequisite(self):
        """Add prerequisite for a course"""
        course = self.prereq_course_input.text().strip()
        prereq = self.prereq_required_input.text().strip()
        
        if not course or not prereq:
            QMessageBox.warning(self, "Validation Error", "Both course codes are required")
            return
        
        success, message = self.db.add_prerequisite(course, prereq)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.prereq_course_input.clear()
            self.prereq_required_input.clear()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def view_program_plan(self):
        """View program plan"""
        program = self.view_program_combo.currentText()
        level = self.view_level_spin.value()
        semester = self.view_semester_spin.value()
        
        courses = self.db.get_program_plan_courses(program, level, semester)
        self.program_plan_table.setRowCount(len(courses))
        
        for i, course in enumerate(courses):
            self.program_plan_table.setItem(i, 0, QTableWidgetItem(course['course_code']))
            self.program_plan_table.setItem(i, 1, QTableWidgetItem(course['name']))
            self.program_plan_table.setItem(i, 2, QTableWidgetItem(str(course['credits'])))
            self.program_plan_table.setItem(i, 3, QTableWidgetItem(str(course['lecture_hours'])))
            self.program_plan_table.setItem(i, 4, QTableWidgetItem(str(course['lab_hours'])))
            self.program_plan_table.setItem(i, 5, QTableWidgetItem("Yes" if course['is_elective'] else "No"))
    
    def add_course_schedule(self):
        """Add course schedule"""
        course_code = self.sched_course_input.text().strip()
        semester = self.sched_semester_input.text().strip()
        day = self.sched_day_combo.currentText()
        start = self.sched_start_input.text().strip()
        end = self.sched_end_input.text().strip()
        room = self.sched_room_input.text().strip()
        is_lab = self.sched_is_lab_check.isChecked()
        
        if not all([course_code, semester, start, end]):
            QMessageBox.warning(self, "Validation Error", "All fields except room are required")
            return
        
        # Get course ID
        courses = self.db.get_all_courses()
        course_id = None
        for c in courses:
            if c['course_code'] == course_code:
                course_id = c['id']
                break
        
        if not course_id:
            QMessageBox.critical(self, "Error", f"Course '{course_code}' not found")
            return
        
        success, message = self.db.add_course_schedule(course_id, day, start, end, room, is_lab, semester)
        
        if success:
            QMessageBox.information(self, "Success", "Schedule added successfully")
            self.sched_course_input.clear()
            self.sched_start_input.clear()
            self.sched_end_input.clear()
            self.sched_room_input.clear()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def view_registrations(self):
        """View all registrations"""
        # This would require a more complex query combining multiple tables
        QMessageBox.information(self, "Info", "View registrations functionality")

