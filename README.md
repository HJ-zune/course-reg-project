# ECE Department Course Registration System

A comprehensive course registration system designed specifically for the ECE Department, built with Python and PyQt6. This system streamlines the course registration process by automatically validating student selections against academic and logistical rules including prerequisites, program plans, course capacity, and schedule conflicts.

## 📋 Project Overview

The ECE Department Course Registration System enables students to plan and register for courses each semester while ensuring compliance with:
- **Prerequisites**: Automatic checking of completed courses
- **Program Plans**: Adherence to ECE programs (Computer, Communications, Power, Biomedical)
- **Course Capacity**: Enrollment limits and availability tracking
- **Schedule Conflicts**: Detection of time overlaps between lectures and labs
- **Credit Limits**: Enforcement of minimum (12) and maximum (18) credits per semester

## 🎯 Key Features

### For Students
- **Course Registration**: Browse and register for courses in their program
- **Visual Timetable**: Weekly calendar view of registered courses
- **Validation**: Real-time checking of prerequisites, conflicts, and capacity
- **Transcript View**: Access to academic history and GPA
- **Drop Courses**: Ability to drop registered courses

### For Administrators
- **Course Management**: Add and manage course catalog
- **Program Plans**: Define curriculum for each program and level
- **Prerequisites**: Set course prerequisites
- **Schedule Management**: Create course schedules with time and room assignments
- **Student Overview**: View all students and their registrations
- **Registration Monitoring**: Track course enrollments and capacity

## 🛠️ Technical Specifications

- **Programming Language**: Python 3.7+
- **GUI Framework**: PyQt6
- **Database**: SQLite3
- **Design Paradigm**: Object-Oriented Programming (OOP)
- **Security**: Password encryption using bcrypt

## 📦 Requirements

Install required dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies
- `PyQt6>=6.0.0` - GUI framework
- `bcrypt>=4.0.0` - Password encryption

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd jiho-shenanigans
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Load Sample Data (Optional but Recommended)

```bash
python load_sample_data.py
```

This will populate the database with:
- 18 sample courses across all ECE programs
- Prerequisites relationships
- Program plans for all 4 programs
- Course schedules for Fall 2025 semester
- 5 sample students with transcripts

### 4. Run the Application

```bash
python main.py
```

Or on Windows, double-click:
```bash
run.bat
```

## 👤 Default Credentials

### Administrator
- **Username**: `admin`
- **Password**: `admin123`

### Student Registration
Students can register through the "Register Student" button on the login screen. You'll need to:
1. Fill in student information (ID, name, email, program, level)
2. Create login credentials (username and password)
3. Login with the created credentials

## 📚 Database Schema

### Tables

**users**
- User authentication with role-based access (Student/Admin)
- Password encryption using bcrypt

**students**
- student_id, name, email, program, level

**courses**
- course_code, name, credits, lecture_hours, lab_hours, max_capacity, description

**prerequisites**
- course_id, prerequisite_course_id

**program_plans**
- program, level, semester, course_id, is_elective

**course_schedules**
- course_id, day, start_time, end_time, room, is_lab, semester_year

**transcripts**
- student_id, course_id, grade, semester_year, passed

**registrations**
- student_id, course_id, semester_year, status

## 🎓 ECE Programs

The system supports four ECE specialization programs:

1. **Computer Engineering** - Focus on software, data structures, and computer architecture
2. **Communications Engineering** - Signal processing and communication systems
3. **Power Engineering** - Power electronics and electrical machines
4. **Biomedical Engineering** - Medical instrumentation and biosignal processing

## 🔍 System Features in Detail

### Registration Validation

The system performs comprehensive validation including:

1. **Credit Hour Limits**: 12-18 credits per semester
2. **Prerequisites Check**: Ensures all required courses are completed
3. **Program Plan Adherence**: Warns if courses are outside program plan
4. **Schedule Conflict Detection**: Prevents time overlaps
5. **Capacity Management**: Blocks registration for full courses

### Timetable Builder

- Visual weekly calendar (Sunday-Thursday)
- Color-coded lectures (green) and labs (blue)
- Shows course code, room, and time
- Real-time updates upon registration/drop

### User Authentication

- Secure login with bcrypt password hashing
- Role-based access control (Student/Admin)
- Separate dashboards for different roles

## 💻 Class Structure

### Core Classes

**MainApp** (PyQt6 QApplication)
- Entry point of the application
- Initializes main window and event loop

**MainWindow** (PyQt6 QMainWindow)
- Manages overall interface
- Handles login and role-specific dashboards

**LoginDialog** (PyQt6 QDialog)
- User authentication
- Student registration

**StudentDashboard** (PyQt6 QWidget)
- Course registration interface
- Timetable viewer
- Transcript display

**AdminDashboard** (PyQt6 QWidget)
- Course and curriculum management
- Program plan configuration
- Student overview

**Course** Class
- Attributes: course_code, name, credits, lecture_hours, lab_hours, max_capacity, prerequisites
- Methods: `check_prerequisites()`, `is_full()`

**Student** Class
- Attributes: student_id, name, email, program, level, transcript
- Methods: `get_completed_credits()`, `add_to_transcript()`, `get_gpa()`

**RegistrationSystem** Class
- Database connection and cursor
- Methods: `validate_schedule()`, `register_student()`, `add_course()`, `get_available_courses()`

## 📖 Usage Guide

### For Students

1. **Login** with your student credentials
2. **Navigate** to "Course Registration" tab
3. **Select courses** from the available list (shows prerequisites status)
4. **Add courses** to your selection
5. **Validate** your schedule (checks all constraints)
6. **Register** for courses once validation passes
7. **View Timetable** to see your weekly schedule
8. **Check Transcript** for academic history and GPA

### For Administrators

1. **Login** with admin credentials
2. **Add Courses** in the Courses tab
3. **Create Program Plans** in the Program Plans tab
4. **Add Prerequisites** for courses
5. **Set Schedules** for each course
6. **Monitor Registrations** in the Registrations tab
7. **View Students** in the Students tab

## 🔧 Validation Rules

### Credit Hours
- **Minimum**: 12 credits per semester
- **Maximum**: 18 credits per semester
- **Validation**: System prevents registration outside these limits

### Prerequisites
- System checks student transcript for completed prerequisites
- Blocks registration if prerequisites not met
- Shows missing prerequisites in course list

### Schedule Conflicts
- Detects time overlaps between lectures and labs
- Checks conflicts on same days
- Prevents double-booking

### Course Capacity
- Tracks current enrollment per course
- Prevents registration when course is full
- Shows available seats

## 📝 Project Structure

```
jiho-shenanigans/
├── main.py                      # Main application entry point
├── database.py                  # Database operations and schema
├── models.py                    # Course, Student, RegistrationSystem classes
├── login_dialog.py              # Login and student registration dialogs
├── admin_dashboard.py           # Administrator interface
├── student_dashboard.py         # Student interface with timetable
├── load_sample_data.py          # Sample data loader
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── run.bat                      # Windows launcher
└── ece_course_registration.db   # SQLite database (created on first run)
```

## 🐛 Error Handling

The system provides comprehensive error handling:

- **Validation Errors**: Clear, actionable messages for constraint violations
- **Database Errors**: Graceful handling of integrity constraints
- **Input Validation**: Checks for required fields and data types
- **User Feedback**: Informative dialogs for all operations

Example error messages:
- "Cannot register for COE310: Missing prerequisites: COE200"
- "Schedule conflict: COE310 Lab overlaps with COE320 Lecture on Tuesday"
- "Course COE200 is full (30/30)"
- "Total credits (21) exceeds maximum of 18"

## 🎨 GUI Features

- **Modern Design**: Clean, professional interface using PyQt6
- **Tab-based Navigation**: Organized by functionality
- **Color Coding**: Visual indicators for status (green=valid, red=error)
- **Responsive Tables**: Sortable columns with proper headers
- **Form Validation**: Real-time input validation
- **Confirmation Dialogs**: Prevents accidental destructive actions

## 🔐 Security Features

- **Password Hashing**: All passwords encrypted with bcrypt
- **Role-Based Access**: Separate permissions for students and admins
- **Input Sanitization**: Protection against SQL injection
- **Session Management**: Secure user authentication

## 📈 Future Enhancements

Possible additions (as per project bonus requirements):
- **Reporting & Analytics Dashboard**: Course demand statistics and enrollment metrics
- **Faculty Module**: Faculty availability and course assignment management
- **Waitlist System**: Automatic enrollment when seats become available
- **Email Notifications**: Registration confirmations and updates
- **What-If Scenarios**: Simulate different program/level choices
- **Bulk Import**: CSV/Excel import for courses and students

## 🐞 Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check PyQt6 installation: `python -c "import PyQt6; print('OK')"`

### Database errors
- Delete `ece_course_registration.db` to start fresh
- Run `load_sample_data.py` to repopulate
- Check file permissions in the directory

### GUI display issues
- Minimum screen resolution: 1200x800
- Try maximizing the window
- Check if system has proper graphics drivers

### Login issues
- Use default admin credentials (admin/admin123)
- Register new student through registration dialog
- Check database for user records

## 📄 License

This project is created as a term project for EE202: Object-Oriented Computer Programming course at the ECE Department.

## 👥 Contributors

Created as part of ECE Department Course Registration System project (Fall 2025).

## 📞 Support

For issues or questions:
1. Check this README for common solutions
2. Review the error messages carefully
3. Ensure all prerequisites are met
4. Verify sample data is loaded correctly

---

**Note**: This system is designed specifically for the ECE Department with support for Computer, Communications, Power, and Biomedical engineering programs. The validation system ensures students register for appropriate courses while meeting all academic requirements.
