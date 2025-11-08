"""
Database module for Course Registration System
Handles all database operations using SQLite
"""

import sqlite3
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Student:
    """Student data class"""
    student_id: str
    name: str
    email: str
    major: str
    id: Optional[int] = None


@dataclass
class Course:
    """Course data class"""
    course_code: str
    name: str
    instructor: str
    credits: int
    max_students: int
    id: Optional[int] = None


@dataclass
class Registration:
    """Registration data class"""
    student_id: int
    course_id: int
    semester: str
    grade: Optional[str] = None
    id: Optional[int] = None


class Database:
    """Database handler for the course registration system"""
    
    def __init__(self, db_name: str = "course_registration.db"):
        """Initialize database connection"""
        self.db_name = db_name
        self.conn = None
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                major TEXT NOT NULL
            )
        """)
        
        # Courses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                instructor TEXT NOT NULL,
                credits INTEGER NOT NULL,
                max_students INTEGER NOT NULL
            )
        """)
        
        # Registrations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                semester TEXT NOT NULL,
                grade TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_id) REFERENCES courses(id),
                UNIQUE(student_id, course_id, semester)
            )
        """)
        
        conn.commit()
        self.close()
    
    # Student operations
    def add_student(self, student: Student) -> bool:
        """Add a new student"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (student_id, name, email, major)
                VALUES (?, ?, ?, ?)
            """, (student.student_id, student.name, student.email, student.major))
            conn.commit()
            self.close()
            return True
        except sqlite3.IntegrityError:
            self.close()
            return False
    
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        self.close()
        return [Student(
            id=row['id'],
            student_id=row['student_id'],
            name=row['name'],
            email=row['email'],
            major=row['major']
        ) for row in rows]
    
    def search_students(self, search_term: str) -> List[Student]:
        """Search students by name or student_id"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM students 
            WHERE name LIKE ? OR student_id LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()
        self.close()
        return [Student(
            id=row['id'],
            student_id=row['student_id'],
            name=row['name'],
            email=row['email'],
            major=row['major']
        ) for row in rows]
    
    def delete_student(self, student_id: int) -> bool:
        """Delete a student"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            self.close()
            return True
        except:
            self.close()
            return False
    
    # Course operations
    def add_course(self, course: Course) -> bool:
        """Add a new course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO courses (course_code, name, instructor, credits, max_students)
                VALUES (?, ?, ?, ?, ?)
            """, (course.course_code, course.name, course.instructor, 
                  course.credits, course.max_students))
            conn.commit()
            self.close()
            return True
        except sqlite3.IntegrityError:
            self.close()
            return False
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        self.close()
        return [Course(
            id=row['id'],
            course_code=row['course_code'],
            name=row['name'],
            instructor=row['instructor'],
            credits=row['credits'],
            max_students=row['max_students']
        ) for row in rows]
    
    def search_courses(self, search_term: str) -> List[Course]:
        """Search courses by name or code"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM courses 
            WHERE name LIKE ? OR course_code LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%'))
        rows = cursor.fetchall()
        self.close()
        return [Course(
            id=row['id'],
            course_code=row['course_code'],
            name=row['name'],
            instructor=row['instructor'],
            credits=row['credits'],
            max_students=row['max_students']
        ) for row in rows]
    
    def delete_course(self, course_id: int) -> bool:
        """Delete a course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            conn.commit()
            self.close()
            return True
        except:
            self.close()
            return False
    
    # Registration operations
    def register_student(self, student_id: int, course_id: int, semester: str) -> Tuple[bool, str]:
        """Register a student for a course"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Check if course is full
        cursor.execute("""
            SELECT c.max_students,
                   COUNT(r.id) as current_count
            FROM courses c
            LEFT JOIN registrations r ON c.id = r.course_id AND r.semester = ?
            WHERE c.id = ?
            GROUP BY c.id
        """, (semester, course_id))
        
        result = cursor.fetchone()
        if result and result['current_count'] >= result['max_students']:
            self.close()
            return False, "Course is full"
        
        # Register the student
        try:
            cursor.execute("""
                INSERT INTO registrations (student_id, course_id, semester)
                VALUES (?, ?, ?)
            """, (student_id, course_id, semester))
            conn.commit()
            self.close()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            self.close()
            return False, "Student already registered for this course"
    
    def get_student_registrations(self, student_id: int) -> List[dict]:
        """Get all courses a student is registered for"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, c.course_code, c.name, c.instructor, 
                   c.credits, r.semester, r.grade
            FROM registrations r
            JOIN courses c ON r.course_id = c.id
            WHERE r.student_id = ?
        """, (student_id,))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def get_course_registrations(self, course_id: int) -> List[dict]:
        """Get all students registered for a course"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, s.student_id, s.name, s.email, 
                   r.semester, r.grade
            FROM registrations r
            JOIN students s ON r.student_id = s.id
            WHERE r.course_id = ?
        """, (course_id,))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]
    
    def drop_registration(self, registration_id: int) -> bool:
        """Drop a course registration"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM registrations WHERE id = ?", (registration_id,))
            conn.commit()
            self.close()
            return True
        except:
            self.close()
            return False
    
    def update_grade(self, registration_id: int, grade: str) -> bool:
        """Update a student's grade for a course"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE registrations 
                SET grade = ? 
                WHERE id = ?
            """, (grade, registration_id))
            conn.commit()
            self.close()
            return True
        except:
            self.close()
            return False

