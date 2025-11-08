"""
ECE Department Course Registration System - Student Dashboard
Provides student interface for course registration and timetable viewing
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTabWidget, QTableWidget, QTableWidgetItem, QLineEdit,
                             QMessageBox, QGroupBox, QHeaderView, QListWidget,
                             QListWidgetItem, QGridLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from database import Database
from models import RegistrationSystem, Student


class StudentDashboard(QWidget):
    """
    Student Dashboard
    Central interface for students to register for courses and view their schedule
    """
    
    def __init__(self, main_window, user_info):
        super().__init__()
        self.main_window = main_window
        self.user_info = user_info
        self.db = Database()
        self.reg_system = RegistrationSystem()
        
        # Get student information
        self.student = self.reg_system.get_student_info(user_info['student_id'])
        if self.student:
            self.student.id = user_info['student_id']  # Set database ID
        
        self.current_semester = "Fall 2025"  # Default semester
        self.selected_courses = []  # Courses selected for registration
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel(f"Welcome, {self.student.name if self.student else 'Student'}")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        if self.student:
            info_label = QLabel(f"{self.student.program} | Level {self.student.level}")
            info_label.setStyleSheet("font-size: 14px; color: #555;")
            header_layout.addWidget(info_label)
        
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.main_window.logout)
        header_layout.addWidget(logout_button)
        
        layout.addLayout(header_layout)
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.create_registration_tab(), "Course Registration")
        self.tabs.addTab(self.create_timetable_tab(), "My Timetable")
        self.tabs.addTab(self.create_transcript_tab(), "My Transcript")
        
        layout.addWidget(self.tabs)
        
        self.setLayout(layout)
    
    def create_registration_tab(self):
        """Create course registration tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Semester selection
        semester_layout = QHBoxLayout()
        semester_layout.addWidget(QLabel("Semester:"))
        self.semester_input = QLineEdit()
        self.semester_input.setText(self.current_semester)
        semester_layout.addWidget(self.semester_input)
        
        set_semester_btn = QPushButton("Set Semester")
        set_semester_btn.clicked.connect(self.update_semester)
        semester_layout.addWidget(set_semester_btn)
        semester_layout.addStretch()
        
        layout.addLayout(semester_layout)
        
        # Main content area (side by side)
        content_layout = QHBoxLayout()
        
        # Left side: Available courses
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Available Courses for Your Program"))
        
        self.available_courses_list = QListWidget()
        self.available_courses_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        left_layout.addWidget(self.available_courses_list)
        
        add_btn = QPushButton("Add Selected Course →")
        add_btn.clicked.connect(self.add_course_to_selection)
        left_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton("Refresh Available Courses")
        refresh_btn.clicked.connect(self.refresh_available_courses)
        left_layout.addWidget(refresh_btn)
        
        content_layout.addLayout(left_layout, 1)
        
        # Right side: Selected courses
        right_layout = QVBoxLayout()
        
        # Selected courses list
        selected_label = QLabel("Selected Courses")
        selected_font = QFont()
        selected_font.setBold(True)
        selected_label.setFont(selected_font)
        right_layout.addWidget(selected_label)
        
        self.selected_courses_list = QListWidget()
        right_layout.addWidget(self.selected_courses_list)
        
        # Credits summary
        self.credits_label = QLabel("Total Credits: 0")
        self.credits_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        right_layout.addWidget(self.credits_label)
        
        # Buttons
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_course_from_selection)
        right_layout.addWidget(remove_btn)
        
        validate_btn = QPushButton("Validate Schedule")
        validate_btn.clicked.connect(self.validate_schedule)
        right_layout.addWidget(validate_btn)
        
        register_btn = QPushButton("Register for Courses")
        register_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        register_btn.clicked.connect(self.register_courses)
        right_layout.addWidget(register_btn)
        
        content_layout.addLayout(right_layout, 1)
        
        layout.addLayout(content_layout)
        
        # Validation messages area
        self.validation_output = QTextEdit()
        self.validation_output.setReadOnly(True)
        self.validation_output.setMaximumHeight(150)
        self.validation_output.setPlaceholderText("Validation messages will appear here...")
        layout.addWidget(self.validation_output)
        
        tab.setLayout(layout)
        
        # Load initial data
        self.refresh_available_courses()
        
        return tab
    
    def create_timetable_tab(self):
        """Create timetable view tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("My Weekly Timetable")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Semester selector
        semester_layout = QHBoxLayout()
        semester_layout.addWidget(QLabel("View Semester:"))
        self.timetable_semester_input = QLineEdit()
        self.timetable_semester_input.setText(self.current_semester)
        semester_layout.addWidget(self.timetable_semester_input)
        
        view_btn = QPushButton("View Timetable")
        view_btn.clicked.connect(self.refresh_timetable)
        semester_layout.addWidget(view_btn)
        semester_layout.addStretch()
        layout.addLayout(semester_layout)
        
        # Timetable grid
        self.timetable_grid = QTableWidget()
        self.timetable_grid.setRowCount(10)  # Time slots
        self.timetable_grid.setColumnCount(5)  # Days
        self.timetable_grid.setHorizontalHeaderLabels([
            "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"
        ])
        
        # Set time labels
        times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        self.timetable_grid.setVerticalHeaderLabels(times)
        
        self.timetable_grid.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.timetable_grid.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.timetable_grid)
        
        # Registered courses list
        reg_courses_label = QLabel("Registered Courses:")
        reg_courses_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(reg_courses_label)
        
        self.registered_courses_table = QTableWidget()
        self.registered_courses_table.setColumnCount(5)
        self.registered_courses_table.setHorizontalHeaderLabels([
            "Course Code", "Name", "Credits", "Status", "Action"
        ])
        self.registered_courses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.registered_courses_table.setMaximumHeight(200)
        layout.addWidget(self.registered_courses_table)
        
        tab.setLayout(layout)
        
        # Load timetable
        self.refresh_timetable()
        
        return tab
    
    def create_transcript_tab(self):
        """Create transcript view tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Header with GPA
        header_layout = QHBoxLayout()
        
        title = QLabel("My Academic Transcript")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        if self.student:
            gpa = self.student.get_gpa()
            completed = self.student.get_completed_credits()
            
            stats_label = QLabel(f"GPA: {gpa:.2f} | Completed Credits: {completed}")
            stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2196F3;")
            header_layout.addWidget(stats_label)
        
        layout.addLayout(header_layout)
        
        # Transcript table
        self.transcript_table = QTableWidget()
        self.transcript_table.setColumnCount(6)
        self.transcript_table.setHorizontalHeaderLabels([
            "Course Code", "Course Name", "Credits", "Grade", "Semester", "Status"
        ])
        self.transcript_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.transcript_table)
        
        tab.setLayout(layout)
        
        # Load transcript
        self.refresh_transcript()
        
        return tab
    
    # Action methods
    def update_semester(self):
        """Update current semester"""
        self.current_semester = self.semester_input.text().strip()
        self.refresh_available_courses()
        QMessageBox.information(self, "Success", f"Semester set to: {self.current_semester}")
    
    def refresh_available_courses(self):
        """Refresh available courses list"""
        if not self.student:
            return
        
        self.available_courses_list.clear()
        
        # Get courses for both semesters of current level
        for semester in [1, 2]:
            courses = self.db.get_program_plan_courses(
                self.student.program, self.student.level, semester
            )
            
            for course in courses:
                # Check prerequisites
                prereqs = self.db.get_course_prerequisites(course['id'])
                can_take = True
                missing_prereqs = []
                
                for prereq in prereqs:
                    if not self.student.has_completed_course(prereq['course_code']):
                        can_take = False
                        missing_prereqs.append(prereq['course_code'])
                
                # Create list item
                item_text = f"{course['course_code']} - {course['name']} ({course['credits']} cr)"
                
                if not can_take:
                    item_text += f" [Missing: {', '.join(missing_prereqs)}]"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, course)  # Store course data
                
                # Color code based on prerequisites
                if not can_take:
                    item.setForeground(QColor("red"))
                else:
                    item.setForeground(QColor("green"))
                
                self.available_courses_list.addItem(item)
    
    def add_course_to_selection(self):
        """Add selected course to registration list"""
        current_item = self.available_courses_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a course first")
            return
        
        course = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Check if already selected
        for selected_course in self.selected_courses:
            if selected_course['id'] == course['id']:
                QMessageBox.warning(self, "Warning", "Course already selected")
                return
        
        self.selected_courses.append(course)
        self.refresh_selected_courses()
    
    def remove_course_from_selection(self):
        """Remove selected course from registration list"""
        current_row = self.selected_courses_list.currentRow()
        if current_row >= 0:
            del self.selected_courses[current_row]
            self.refresh_selected_courses()
    
    def refresh_selected_courses(self):
        """Refresh selected courses list"""
        self.selected_courses_list.clear()
        total_credits = 0
        
        for course in self.selected_courses:
            item_text = f"{course['course_code']} - {course['name']} ({course['credits']} cr)"
            self.selected_courses_list.addItem(item_text)
            total_credits += course['credits']
        
        self.credits_label.setText(f"Total Credits: {total_credits}")
        
        # Color code based on credit limits
        if total_credits < 12:
            self.credits_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        elif total_credits > 18:
            self.credits_label.setStyleSheet("font-size: 14px; font-weight: bold; color: orange;")
        else:
            self.credits_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
    
    def validate_schedule(self):
        """Validate selected courses"""
        if not self.selected_courses:
            QMessageBox.warning(self, "Warning", "No courses selected")
            return
        
        if not self.student:
            QMessageBox.critical(self, "Error", "Student information not found")
            return
        
        # Validate schedule
        is_valid, errors = self.reg_system.validate_schedule(
            self.student, self.selected_courses, self.current_semester
        )
        
        # Display results
        self.validation_output.clear()
        
        if is_valid:
            self.validation_output.setStyleSheet("color: green;")
            self.validation_output.setText("✓ Schedule is valid! You can proceed with registration.")
        else:
            self.validation_output.setStyleSheet("color: red;")
            error_text = "✗ Schedule validation failed:\n\n"
            error_text += "\n".join(f"• {error}" for error in errors)
            self.validation_output.setText(error_text)
    
    def register_courses(self):
        """Register for selected courses"""
        if not self.selected_courses:
            QMessageBox.warning(self, "Warning", "No courses selected")
            return
        
        if not self.student:
            QMessageBox.critical(self, "Error", "Student information not found")
            return
        
        # Validate first
        is_valid, errors = self.reg_system.validate_schedule(
            self.student, self.selected_courses, self.current_semester
        )
        
        if not is_valid:
            reply = QMessageBox.question(
                self, "Validation Errors",
                "There are validation errors. Do you want to see them?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.validate_schedule()
            return
        
        # Register
        success, message = self.reg_system.register_student(
            self.student, self.selected_courses, self.current_semester
        )
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.selected_courses.clear()
            self.refresh_selected_courses()
            self.refresh_timetable()
        else:
            QMessageBox.critical(self, "Error", message)
    
    def refresh_timetable(self):
        """Refresh timetable display"""
        semester = self.timetable_semester_input.text().strip()
        
        if not self.student:
            return
        
        # Clear timetable
        for row in range(self.timetable_grid.rowCount()):
            for col in range(self.timetable_grid.columnCount()):
                self.timetable_grid.setItem(row, col, QTableWidgetItem(""))
        
        # Get registered courses
        registrations = self.db.get_student_registrations(self.student.id, semester)
        
        # Update registered courses table
        self.registered_courses_table.setRowCount(len(registrations))
        
        for i, reg in enumerate(registrations):
            self.registered_courses_table.setItem(i, 0, QTableWidgetItem(reg['course_code']))
            self.registered_courses_table.setItem(i, 1, QTableWidgetItem(reg['name']))
            self.registered_courses_table.setItem(i, 2, QTableWidgetItem(str(reg['credits'])))
            self.registered_courses_table.setItem(i, 3, QTableWidgetItem(reg['status']))
            
            # Add drop button
            drop_btn = QPushButton("Drop")
            drop_btn.clicked.connect(lambda checked, reg_id=reg['registration_id']: self.drop_course(reg_id))
            self.registered_courses_table.setCellWidget(i, 4, drop_btn)
            
            # Get schedule and populate timetable
            schedule = self.db.get_course_schedule(reg['id'], semester)
            for sched in schedule:
                # Map day to column
                day_map = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4}
                col = day_map.get(sched['day'], -1)
                
                if col >= 0:
                    # Calculate row from time
                    try:
                        start_hour = int(sched['start_time'].split(':')[0])
                        row = start_hour - 8  # Assuming starts at 8:00
                        
                        if 0 <= row < self.timetable_grid.rowCount():
                            cell_text = f"{reg['course_code']}\n{sched['room'] or ''}"
                            if sched['is_lab']:
                                cell_text += "\n(Lab)"
                            
                            item = QTableWidgetItem(cell_text)
                            item.setBackground(QColor("#4CAF50" if not sched['is_lab'] else "#2196F3"))
                            item.setForeground(QColor("white"))
                            self.timetable_grid.setItem(row, col, item)
                    except:
                        pass
    
    def drop_course(self, registration_id):
        """Drop a registered course"""
        reply = QMessageBox.question(
            self, "Confirm Drop",
            "Are you sure you want to drop this course?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.db.drop_registration(registration_id)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.refresh_timetable()
            else:
                QMessageBox.critical(self, "Error", message)
    
    def refresh_transcript(self):
        """Refresh transcript display"""
        if not self.student:
            return
        
        transcript = self.student.transcript
        self.transcript_table.setRowCount(len(transcript))
        
        for i, entry in enumerate(transcript):
            self.transcript_table.setItem(i, 0, QTableWidgetItem(entry['course_code']))
            self.transcript_table.setItem(i, 1, QTableWidgetItem(entry['name']))
            self.transcript_table.setItem(i, 2, QTableWidgetItem(str(entry['credits'])))
            self.transcript_table.setItem(i, 3, QTableWidgetItem(entry['grade'] or 'N/A'))
            self.transcript_table.setItem(i, 4, QTableWidgetItem(entry['semester_year']))
            self.transcript_table.setItem(i, 5, QTableWidgetItem("Passed" if entry['passed'] else "Failed"))
            
            # Color code by grade
            if entry['passed']:
                for col in range(6):
                    item = self.transcript_table.item(i, col)
                    if item:
                        item.setForeground(QColor("green"))
            else:
                for col in range(6):
                    item = self.transcript_table.item(i, col)
                    if item:
                        item.setForeground(QColor("red"))

