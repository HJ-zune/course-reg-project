"""
ECE Department Course Registration System - Database Module
Handles all database operations using SQLite3
"""

import sqlite3
from typing import List, Tuple, Optional, Dict
import bcrypt


class Database:
    """Database handler for the course registration system"""
    
    def __init__(self, db_name: str = "ece_course_registration.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.create_tables()
        self.insert_default_admin()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create all database tables if they don't exist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Users table for authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Student', 'Admin')),
                student_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                program TEXT NOT NULL CHECK(program IN ('Computer', 'Communications', 'Power', 'Biomedical')),
                level INTEGER NOT NULL CHECK(level >= 1 AND level <= 4)
            )
        """)
        
        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                credits INTEGER NOT NULL CHECK(credits > 0),
                lecture_hours INTEGER NOT NULL DEFAULT 0,
                lab_hours INTEGER NOT NULL DEFAULT 0,
                max_capacity INTEGER NOT NULL CHECK(max_capacity > 0),
                description TEXT
            )
        """)
        
        # Prerequisites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prerequisites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                prerequisite_course_id INTEGER NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                FOREIGN KEY (prerequisite_course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(course_id, prerequisite_course_id)
            )
        """)
        
        # Program plans table (maps courses to programs and levels)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS program_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                program TEXT NOT NULL CHECK(program IN ('Computer', 'Communications', 'Power', 'Biomedical')),
                level INTEGER NOT NULL CHECK(level >= 1 AND level <= 4),
                semester INTEGER NOT NULL CHECK(semester IN (1, 2)),
                course_id INTEGER NOT NULL,
                is_elective BOOLEAN DEFAULT 0,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(program, level, semester, course_id)
            )
        """)
        
        # Course schedules table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                day TEXT NOT NULL CHECK(day IN ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday')),
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                room TEXT,
                is_lab BOOLEAN DEFAULT 0,
                semester_year TEXT NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        """)
        
        # Transcripts table (student completed courses)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                grade TEXT,
                semester_year TEXT NOT NULL,
                passed BOOLEAN DEFAULT 0,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id, semester_year)
            )
        """)
        
        # Registrations table (current semester registrations)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                semester_year TEXT NOT NULL,
                status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Dropped')),
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                UNIQUE(student_id, course_id, semester_year)
            )
        """)
        
        conn.commit()
        self.close()
    
    def insert_default_admin(self):
        """Insert default admin user if not exists"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Check if admin exists
        cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
        if cursor.fetchone() is None:
            # Create default admin (username: admin, password: admin123)
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, ('admin', password_hash, 'Admin'))
            conn.commit()
        
        self.close()
    
    # User Authentication Methods
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user info"""
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            self.close()
            return {
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'student_id': user['student_id']
            }
        
        self.close()
        return None
    
    def register_user(self, username: str, password: str, role: str, student_id: Optional[int] = None) -> Tuple[bool, str]:
        """Register a new user"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, student_id)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, role, student_id))
            
            conn.commit()
            self.close()
            return True, "User registered successfully"
        except sqlite3.IntegrityError:
            self.close()
            return False, "Username already exists"
    
    # Student Methods
    def add_student(self, student_id: str, name: str, email: str, program: str, level: int) -> Tuple[bool, str]:
        """Add a new student"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (student_id, name, email, program, level)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, name, email, program, level))
            conn.commit()
            self.close()
            return True, "Student added successfully"
        except sqlite3.IntegrityError as e:
            self.close()
            return False, f"Error: {str(e)}"
    
    def get_student_by_id(self, db_id: int) -> Optional[Dict]:
        """Get student by database ID"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (db_id,))
        student = cursor.fetchone()
        self.close()
        return dict(student) if student else None
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        self.close()
        return [dict(row) for row in students]
    
    # Course Methods
    def add_course(self, course_code: str, name: str, credits: int, lecture_hours: int, 
                   lab_hours: int, max_capacity: int, description: str = "") -> Tuple[bool, str]:
        """Add a new course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO courses (course_code, name, credits, lecture_hours, lab_hours, max_capacity, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (course_code, name, credits, lecture_hours, lab_hours, max_capacity, description))
            conn.commit()
            self.close()
            return True, "Course added successfully"
        except sqlite3.IntegrityError:
            self.close()
            return False, f"Course code '{course_code}' already exists"
    
    def get_all_courses(self) -> List[Dict]:
        """Get all courses"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        self.close()
        return [dict(row) for row in courses]
    
    def get_course_by_id(self, course_id: int) -> Optional[Dict]:
        """Get course by ID"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        course = cursor.fetchone()
        self.close()
        return dict(course) if course else None
    
    # Prerequisite Methods
    def add_prerequisite(self, course_code: str, prerequisite_code: str) -> Tuple[bool, str]:
        """Add a prerequisite for a course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Get course IDs
            cursor.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,))
            course = cursor.fetchone()
            cursor.execute("SELECT id FROM courses WHERE course_code = ?", (prerequisite_code,))
            prereq = cursor.fetchone()
            
            if not course:
                self.close()
                return False, f"Course '{course_code}' does not exist"
            if not prereq:
                self.close()
                return False, f"Prerequisite course '{prerequisite_code}' is not a valid course"
            
            cursor.execute("""
                INSERT INTO prerequisites (course_id, prerequisite_course_id)
                VALUES (?, ?)
            """, (course['id'], prereq['id']))
            
            conn.commit()
            self.close()
            return True, "Prerequisite added successfully"
        except sqlite3.IntegrityError:
            self.close()
            return False, "Prerequisite already exists"
    
    def get_course_prerequisites(self, course_id: int) -> List[Dict]:
        """Get all prerequisites for a course"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.* FROM courses c
            JOIN prerequisites p ON c.id = p.prerequisite_course_id
            WHERE p.course_id = ?
        """, (course_id,))
        prereqs = cursor.fetchall()
        self.close()
        return [dict(row) for row in prereqs]
    
    # Program Plan Methods
    def add_to_program_plan(self, program: str, level: int, semester: int, 
                            course_code: str, is_elective: bool = False) -> Tuple[bool, str]:
        """Add a course to a program plan"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,))
            course = cursor.fetchone()
            
            if not course:
                self.close()
                return False, f"Course '{course_code}' does not exist"
            
            cursor.execute("""
                INSERT INTO program_plans (program, level, semester, course_id, is_elective)
                VALUES (?, ?, ?, ?, ?)
            """, (program, level, semester, course['id'], is_elective))
            
            conn.commit()
            self.close()
            return True, "Course added to program plan"
        except sqlite3.IntegrityError:
            self.close()
            return False, "Course already in program plan"
    
    def get_program_plan_courses(self, program: str, level: int, semester: int) -> List[Dict]:
        """Get courses for a specific program, level, and semester"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, pp.is_elective FROM courses c
            JOIN program_plans pp ON c.id = pp.course_id
            WHERE pp.program = ? AND pp.level = ? AND pp.semester = ?
        """, (program, level, semester))
        courses = cursor.fetchall()
        self.close()
        return [dict(row) for row in courses]
    
    # Transcript Methods
    def add_to_transcript(self, student_id: int, course_id: int, grade: str, 
                         semester_year: str, passed: bool) -> Tuple[bool, str]:
        """Add a course to student's transcript"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transcripts (student_id, course_id, grade, semester_year, passed)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, course_id, grade, semester_year, passed))
            conn.commit()
            self.close()
            return True, "Added to transcript"
        except sqlite3.IntegrityError:
            self.close()
            return False, "Course already in transcript"
    
    def get_student_transcript(self, student_id: int) -> List[Dict]:
        """Get student's complete transcript"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, t.grade, t.semester_year, t.passed
            FROM transcripts t
            JOIN courses c ON t.course_id = c.id
            WHERE t.student_id = ?
        """, (student_id,))
        transcript = cursor.fetchall()
        self.close()
        return [dict(row) for row in transcript]
    
    # Registration Methods
    def register_student_for_course(self, student_id: int, course_id: int, 
                                   semester_year: str) -> Tuple[bool, str]:
        """Register a student for a course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO registrations (student_id, course_id, semester_year, status)
                VALUES (?, ?, ?, 'Pending')
            """, (student_id, course_id, semester_year))
            conn.commit()
            self.close()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            self.close()
            return False, "Student already registered for this course"
    
    def get_student_registrations(self, student_id: int, semester_year: str) -> List[Dict]:
        """Get student's current registrations"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, r.status, r.id as registration_id
            FROM registrations r
            JOIN courses c ON r.course_id = c.id
            WHERE r.student_id = ? AND r.semester_year = ? AND r.status != 'Dropped'
        """, (student_id, semester_year))
        registrations = cursor.fetchall()
        self.close()
        return [dict(row) for row in registrations]
    
    def drop_registration(self, registration_id: int) -> Tuple[bool, str]:
        """Drop a course registration"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE registrations 
                SET status = 'Dropped'
                WHERE id = ?
            """, (registration_id,))
            conn.commit()
            self.close()
            return True, "Course dropped successfully"
        except:
            self.close()
            return False, "Failed to drop course"
    
    def get_course_enrollment_count(self, course_id: int, semester_year: str) -> int:
        """Get current enrollment count for a course"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM registrations
            WHERE course_id = ? AND semester_year = ? AND status != 'Dropped'
        """, (course_id, semester_year))
        result = cursor.fetchone()
        self.close()
        return result['count'] if result else 0
    
    # Schedule Methods
    def add_course_schedule(self, course_id: int, day: str, start_time: str, 
                          end_time: str, room: str, is_lab: bool, semester_year: str) -> Tuple[bool, str]:
        """Add a schedule for a course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO course_schedules (course_id, day, start_time, end_time, room, is_lab, semester_year)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (course_id, day, start_time, end_time, room, is_lab, semester_year))
            conn.commit()
            self.close()
            return True, "Schedule added"
        except Exception as e:
            self.close()
            return False, str(e)
    
    def get_course_schedule(self, course_id: int, semester_year: str) -> List[Dict]:
        """Get schedule for a course"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM course_schedules
            WHERE course_id = ? AND semester_year = ?
        """, (course_id, semester_year))
        schedules = cursor.fetchall()
        self.close()
        return [dict(row) for row in schedules]
