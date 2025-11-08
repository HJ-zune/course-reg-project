"""
Sample Data Script for Course Registration System
Run this script to populate the database with sample students and courses
"""

from database import Database, Student, Course


def add_sample_data():
    """Add sample students and courses to the database"""
    db = Database()
    
    print("Adding sample data to the database...")
    
    # Sample students
    students = [
        Student(student_id="S001", name="Alice Johnson", email="alice@university.edu", major="Computer Science"),
        Student(student_id="S002", name="Bob Smith", email="bob@university.edu", major="Mathematics"),
        Student(student_id="S003", name="Carol Williams", email="carol@university.edu", major="Physics"),
        Student(student_id="S004", name="David Brown", email="david@university.edu", major="Computer Science"),
        Student(student_id="S005", name="Emma Davis", email="emma@university.edu", major="Engineering"),
    ]
    
    for student in students:
        if db.add_student(student):
            print(f"✓ Added student: {student.name}")
        else:
            print(f"✗ Student {student.student_id} already exists")
    
    # Sample courses
    courses = [
        Course(course_code="CS101", name="Introduction to Programming", 
               instructor="Dr. Anderson", credits=3, max_students=30),
        Course(course_code="CS201", name="Data Structures", 
               instructor="Dr. Martinez", credits=4, max_students=25),
        Course(course_code="MATH101", name="Calculus I", 
               instructor="Prof. Johnson", credits=4, max_students=40),
        Course(course_code="PHYS101", name="Physics I", 
               instructor="Dr. Lee", credits=4, max_students=35),
        Course(course_code="ENG101", name="Engineering Design", 
               instructor="Prof. Wilson", credits=3, max_students=20),
    ]
    
    for course in courses:
        if db.add_course(course):
            print(f"✓ Added course: {course.name}")
        else:
            print(f"✗ Course {course.course_code} already exists")
    
    print("\nSample data added successfully!")
    print("You can now run main.py to start the application.")


if __name__ == "__main__":
    add_sample_data()

