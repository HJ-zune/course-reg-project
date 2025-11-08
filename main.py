"""
ECE Department Course Registration System - Main Application
PyQt6-based GUI application for course registration
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QWidget, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import Database
from login_dialog import LoginDialog
from admin_dashboard import AdminDashboard
from student_dashboard import StudentDashboard


class MainApp(QApplication):
    """
    Main Application class
    Entry point for the ECE Course Registration System
    """
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("ECE Course Registration System")
        self.setStyle('Fusion')  # Modern look
        
        # Initialize database
        self.db = Database()
        
        # Create and show main window
        self.main_window = MainWindow()
        self.main_window.show()


class MainWindow(QMainWindow):
    """
    Main Window class
    Manages the overall graphical interface including login and dashboards
    """
    
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.db = Database()
        
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ECE Department Course Registration System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget with stacked layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # Will add dashboards after login
        self.admin_dashboard = None
        self.student_dashboard = None
    
    def show_login(self):
        """Show login dialog"""
        login_dialog = LoginDialog(self)
        if login_dialog.exec():
            user_info = login_dialog.user_info
            self.current_user = user_info
            self.load_dashboard(user_info)
        else:
            # User cancelled login, exit application
            sys.exit(0)
    
    def load_dashboard(self, user_info: dict):
        """
        Load appropriate dashboard based on user role
        
        Args:
            user_info: Dictionary containing user information
        """
        # Clear existing widgets
        while self.stacked_widget.count() > 0:
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        if user_info['role'] == 'Admin':
            self.admin_dashboard = AdminDashboard(self, user_info)
            self.stacked_widget.addWidget(self.admin_dashboard)
        else:  # Student role
            self.student_dashboard = StudentDashboard(self, user_info)
            self.stacked_widget.addWidget(self.student_dashboard)
        
        self.stacked_widget.setCurrentIndex(0)
    
    def logout(self):
        """Logout current user"""
        reply = QMessageBox.question(
            self, 'Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.show_login()


def main():
    """Main entry point"""
    app = MainApp(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
