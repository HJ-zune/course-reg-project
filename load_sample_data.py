"""
Load Sample Data for ECE Course Registration System
Run this script to populate the database with sample courses, program plans, and schedules
"""

from database import Database
from models import Course

def load_sample_data():
    """Load comprehensive sample data"""
    db = Database()
    
    print("Loading sample data for ECE Department Course Registration System...")
    print("="*60)
    
    # Sample courses
    courses = [
        # Level 1
        ("COE100", "Introduction to Engineering", 3, 2, 2, 40, "Basic engineering concepts"),
        ("MATH101", "Calculus I", 4, 4, 0, 50, "Differential calculus"),
        ("PHYS101", "Physics I", 4, 3, 2, 45, "Mechanics and thermodynamics"),
        ("CHEM101", "General Chemistry", 3, 2, 2, 40, "Basic chemistry principles"),
        
        # Level 2 - Computer Track
        ("COE200", "Programming Fundamentals", 4, 3, 2, 35, "Introduction to programming in C++"),
        ("COE210", "Digital Logic Design", 4, 3, 2, 30, "Boolean algebra and logic circuits"),
        ("MATH201", "Calculus II", 4, 4, 0, 45, "Integral calculus"),
        ("COE220", "Circuit Analysis", 4, 3, 2, 35, "AC/DC circuit analysis"),
        
        # Level 3 - Computer Track
        ("COE310", "Data Structures", 4, 3, 2, 30, "Advanced data structures and algorithms"),
        ("COE320", "Computer Architecture", 4, 3, 2, 30, "CPU design and organization"),
        ("COE330", "Embedded Systems", 4, 3, 2, 25, "Microcontroller programming"),
        ("COE340", "Operating Systems", 4, 3, 2, 30, "OS concepts and design"),
        
        # Level 3 - Communications Track
        ("COE350", "Signal Processing", 4, 3, 2, 30, "Digital signal processing fundamentals"),
        ("COE360", "Communication Systems", 4, 3, 2, 30, "Analog and digital communications"),
        
        # Level 3 - Power Track
        ("COE370", "Power Electronics", 4, 3, 2, 25, "Power conversion and control"),
        ("COE380", "Electrical Machines", 4, 3, 2, 25, "DC and AC machines"),
        
        # Level 3 - Biomedical Track
        ("COE390", "Biomedical Instrumentation", 4, 3, 2, 20, "Medical device design"),
        ("COE395", "Biosignal Processing", 4, 3, 2, 20, "Analysis of biological signals"),
    ]
    
    print("\n1. Adding Courses...")
    for course_data in courses:
        success, msg = db.add_course(*course_data)
        if success:
            print(f"   [+] Added: {course_data[0]} - {course_data[1]}")
        else:
            print(f"   [-] {msg}")
    
    # Add prerequisites
    print("\n2. Adding Prerequisites...")
    prerequisites = [
        ("COE310", "COE200"),  # Data Structures requires Programming
        ("COE320", "COE210"),  # Computer Architecture requires Digital Logic
        ("COE330", "COE200"),  # Embedded Systems requires Programming
        ("COE340", "COE310"),  # Operating Systems requires Data Structures
        ("COE350", "MATH201"), # Signal Processing requires Calculus II
        ("COE360", "COE350"),  # Communication Systems requires Signal Processing
        ("MATH201", "MATH101"), # Calculus II requires Calculus I
        ("COE220", "PHYS101"), # Circuit Analysis requires Physics I
    ]
    
    for course, prereq in prerequisites:
        success, msg = db.add_prerequisite(course, prereq)
        if success:
            print(f"   [+] {course} requires {prereq}")
        else:
            print(f"   [-] {msg}")
    
    # Add to program plans
    print("\n3. Adding to Program Plans...")
    
    # Level 1 (Common for all programs)
    level1_courses = ["COE100", "MATH101", "PHYS101", "CHEM101"]
    for program in ["Computer", "Communications", "Power", "Biomedical"]:
        for i, course_code in enumerate(level1_courses):
            semester = 1 if i < 2 else 2
            success, msg = db.add_to_program_plan(program, 1, semester, course_code, False)
            if success:
                print(f"   [+] Added {course_code} to {program} L1 S{semester}")
    
    # Level 2 (Common)
    level2_courses = [
        ("COE200", 1), ("COE210", 1),
        ("MATH201", 2), ("COE220", 2)
    ]
    for program in ["Computer", "Communications", "Power", "Biomedical"]:
        for course_code, semester in level2_courses:
            success, msg = db.add_to_program_plan(program, 2, semester, course_code, False)
            if success:
                print(f"   [+] Added {course_code} to {program} L2 S{semester}")
    
    # Level 3 - Program specific
    computer_l3 = [("COE310", 1), ("COE320", 1), ("COE330", 2), ("COE340", 2)]
    for course_code, semester in computer_l3:
        success, msg = db.add_to_program_plan("Computer", 3, semester, course_code, False)
        if success:
            print(f"   [+] Added {course_code} to Computer L3 S{semester}")
    
    comm_l3 = [("COE350", 1), ("COE360", 2)]
    for course_code, semester in comm_l3:
        success, msg = db.add_to_program_plan("Communications", 3, semester, course_code, False)
        if success:
            print(f"   [+] Added {course_code} to Communications L3 S{semester}")
    
    power_l3 = [("COE370", 1), ("COE380", 2)]
    for course_code, semester in power_l3:
        success, msg = db.add_to_program_plan("Power", 3, semester, course_code, False)
        if success:
            print(f"   [+] Added {course_code} to Power L3 S{semester}")
    
    bio_l3 = [("COE390", 1), ("COE395", 2)]
    for course_code, semester in bio_l3:
        success, msg = db.add_to_program_plan("Biomedical", 3, semester, course_code, False)
        if success:
            print(f"   [+] Added {course_code} to Biomedical L3 S{semester}")
    
    # Add sample schedules for Fall 2025
    print("\n4. Adding Course Schedules...")
    
    # Get all courses
    all_courses = db.get_all_courses()
    course_map = {c['course_code']: c['id'] for c in all_courses}
    
    schedules = [
        ("COE100", "Sunday", "08:00", "10:00", "A101", False),
        ("COE100", "Tuesday", "10:00", "12:00", "Lab1", True),
        ("COE200", "Monday", "08:00", "10:00", "A201", False),
        ("COE200", "Wednesday", "14:00", "16:00", "Lab2", True),
        ("COE310", "Sunday", "10:00", "12:00", "A301", False),
        ("COE310", "Tuesday", "14:00", "16:00", "Lab3", True),
        ("COE320", "Monday", "10:00", "12:00", "A302", False),
        ("COE320", "Thursday", "08:00", "10:00", "Lab3", True),
    ]
    
    for course_code, day, start, end, room, is_lab in schedules:
        if course_code in course_map:
            success, msg = db.add_course_schedule(
                course_map[course_code], day, start, end, room, is_lab, "Fall 2025"
            )
            if success:
                lab_str = "(Lab)" if is_lab else "(Lecture)"
                print(f"   [+] Added schedule for {course_code} {day} {start}-{end} {lab_str}")
    
    # Add sample students with transcripts
    print("\n5. Adding Sample Students...")
    
    students = [
        ("2021001", "Ahmed Hassan", "ahmed.hassan@ece.edu", "Computer", 3),
        ("2021002", "Fatima Ali", "fatima.ali@ece.edu", "Communications", 3),
        ("2021003", "Mohammed Khalid", "mohammed.khalid@ece.edu", "Power", 3),
        ("2022001", "Sara Ahmed", "sara.ahmed@ece.edu", "Biomedical", 2),
        ("2022002", "Omar Said", "omar.said@ece.edu", "Computer", 2),
    ]
    
    for student_data in students:
        success, msg = db.add_student(*student_data)
        if success:
            print(f"   [+] Added student: {student_data[0]} - {student_data[1]}")
        else:
            print(f"   [-] {msg}")
    
    # Add transcripts for Level 3 students (they completed Level 1 and 2)
    print("\n6. Adding Sample Transcripts...")
    
    all_students = db.get_all_students()
    student_map = {s['student_id']: s['id'] for s in all_students}
    
    # Student 2021001 (Level 3) completed Level 1 and 2 courses
    if "2021001" in student_map:
        completed_courses = ["COE100", "MATH101", "PHYS101", "CHEM101", "COE200", "COE210", "MATH201", "COE220"]
        for course_code in completed_courses:
            if course_code in course_map:
                success, msg = db.add_to_transcript(
                    student_map["2021001"], course_map[course_code], "A", "Past", True
                )
                if success:
                    print(f"   [+] Added {course_code} to 2021001's transcript")
    
    print("\n" + "="*60)
    print("Sample data loaded successfully!")
    print("\nDefault Login Credentials:")
    print("   Admin: username='admin', password='admin123'")
    print("\nTo create student accounts, register through the login screen.")
    print("="*60)

if __name__ == "__main__":
    load_sample_data()

