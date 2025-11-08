# Quick Start Guide

## ✅ Your project is ready!

All requirements from the PDF have been implemented with PyQt6.

## 🚀 Running the Application

### Option 1: Command Line
```bash
cd jiho-shenanigans
python main.py
```

### Option 2: Windows Batch File
Double-click `run.bat` in the jiho-shenanigans folder

## 🔑 Login Credentials

### Administrator Account
- **Username**: `admin`
- **Password**: `admin123`

### Student Account
Click "Register Student" on the login screen to create a new student account.

## 📚 What's Already Loaded

The database includes:
- ✅ 18 courses across all ECE programs
- ✅ 8 prerequisite relationships
- ✅ Complete program plans for all 4 programs (Computer, Communications, Power, Biomedical)
- ✅ 8 course schedules for Fall 2025
- ✅ 5 sample students with transcripts
- ✅ Default admin account

## 🎯 Testing the System

### As Admin:
1. Login with admin credentials
2. Go to "Courses" tab to see all courses
3. Go to "Program Plans" tab to view curriculum
4. Add new courses, prerequisites, or schedules

### As Student:
1. Click "Register Student" on login screen
2. Fill in your information:
   - Student ID (e.g., 2023001)
   - Name, Email
   - Select Program (Computer/Communications/Power/Biomedical)
   - Select Level (1-4)
   - Create username and password
3. Login with your new credentials
4. Go to "Course Registration" tab
5. Select courses from the available list
6. Click "Validate Schedule" to check for errors
7. Click "Register for Courses" to enroll
8. View your timetable in "My Timetable" tab

## 🎓 Sample Student for Testing

One student (Ahmed Hassan, ID: 2021001) already has a transcript with completed Level 1 and 2 courses. You can:
1. Create an account for him (use student ID: 2021001)
2. Register for Level 3 Computer courses (COE310, COE320, COE330, COE340)
3. See the prerequisites validation in action!

## 📋 Key Features to Demo

### Validation Features
1. **Credit Limits**: Try selecting courses totaling less than 12 or more than 18 credits
2. **Prerequisites**: Try registering for COE310 without completing COE200
3. **Schedule Conflicts**: System detects time overlaps
4. **Course Capacity**: Shows when courses are full

### Visual Features
- **Timetable**: Color-coded weekly schedule (green=lecture, blue=lab)
- **Transcript**: Shows GPA and completed courses
- **Real-time Validation**: Instant feedback on course selection

## 📁 Project Files

- `main.py` - Application entry point
- `database.py` - Database schema and operations
- `models.py` - Core classes (Course, Student, RegistrationSystem)
- `login_dialog.py` - Authentication dialogs
- `admin_dashboard.py` - Admin interface
- `student_dashboard.py` - Student interface with timetable
- `load_sample_data.py` - Sample data loader
- `README.md` - Complete documentation
- `PROJECT_SUMMARY.md` - Implementation summary

## 🐛 Troubleshooting

**Application won't start:**
```bash
pip install -r requirements.txt
```

**Want to reset the database:**
```bash
del ece_course_registration.db
python load_sample_data.py
```

**Need to check if PyQt6 is installed:**
```bash
python -c "import PyQt6; print('PyQt6 is installed')"
```

## 📞 Dependencies

All installed:
- ✅ PyQt6 (6.10.0)
- ✅ bcrypt (3.2.0)
- ✅ Python 3.12
- ✅ SQLite3 (built-in)

## 🎉 Ready to Go!

Everything is set up and ready. Just run:
```bash
python main.py
```

And start exploring the system!

---

For more detailed information, see:
- **README.md** - Full documentation
- **PROJECT_SUMMARY.md** - Implementation details

