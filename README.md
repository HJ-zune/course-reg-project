# Course Registration System

A simple and user-friendly course registration system built with Python and tkinter.

## Features

### Student Management
- Add new students with ID, name, email, and major
- View all students in a sortable list
- Search students by name or student ID
- Delete student records
- View student course registrations (double-click on a student)

### Course Management
- Add new courses with code, name, instructor, credits, and capacity
- View all courses in a sortable list
- Search courses by name or course code
- Delete course records
- View enrolled students (double-click on a course)

### Course Registration
- Register students for courses
- Automatic capacity checking (prevents over-enrollment)
- Semester-based registration
- View all registrations
- Drop course registrations
- Update grades for completed courses

## Requirements

- Python 3.7 or higher
- No external packages required (uses only Python standard library)

## Installation

1. Ensure you have Python 3.7+ installed:
```bash
python --version
```

2. Clone or download this project

3. Navigate to the project directory:
```bash
cd jiho-shenanigans
```

## Usage

Run the application:
```bash
python main.py
```

### Getting Started

1. **Add Students**: Go to the "Students" tab and fill in the student details, then click "Add Student"

2. **Add Courses**: Go to the "Courses" tab and fill in the course details, then click "Add Course"

3. **Register Students**: Go to the "Register for Course" tab, select a student and a course, enter the semester, and click "Register"

4. **View Registrations**: 
   - Double-click on a student to see their registered courses
   - Double-click on a course to see enrolled students
   - View all registrations in the "Register for Course" tab

5. **Manage Grades**: Right-click on a registration in the "Register for Course" tab to update grades or drop the registration

## Database

The application uses SQLite for data storage. The database file `course_registration.db` will be created automatically in the same directory as the application.

### Database Schema

**Students Table**
- id (Primary Key)
- student_id (Unique)
- name
- email
- major

**Courses Table**
- id (Primary Key)
- course_code (Unique)
- name
- instructor
- credits
- max_students

**Registrations Table**
- id (Primary Key)
- student_id (Foreign Key)
- course_id (Foreign Key)
- semester
- grade

## Features Details

### Search Functionality
- Search for students by name or student ID
- Search for courses by name or course code
- Clear search to view all records

### Capacity Management
- Courses have a maximum student capacity
- System prevents registration when course is full
- Current enrollment is tracked per semester

### Duplicate Prevention
- Student IDs must be unique
- Course codes must be unique
- Students cannot register for the same course twice in the same semester

### Grade Management
- Grades can be updated after registration
- Right-click on any registration to update the grade
- Grades are optional (shows as blank if not entered)

## Tips

- Use the search feature to quickly find students or courses
- Double-click on students/courses to see detailed registration information
- Right-click on registrations for quick actions (drop or update grade)
- The "Refresh" buttons reload data from the database

## Troubleshooting

**Application won't start:**
- Make sure Python 3.7+ is installed
- Ensure tkinter is available (usually comes with Python)

**Database errors:**
- Delete `course_registration.db` to start fresh
- Make sure you have write permissions in the directory

**Display issues:**
- The application requires a minimum screen resolution of 1000x600
- Try maximizing the window for better viewing

## Project Structure

```
course-reg-project/
├── main.py              # Main GUI application
├── database.py          # Database operations and models
├── requirements.txt     # Project requirements
├── README.md           # This file
└── course_registration.db  # SQLite database (created on first run)
```

## License

This is a simple educational project for course management purposes.

## Author

Created as a term project for Course Registration System

