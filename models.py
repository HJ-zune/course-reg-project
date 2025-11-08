"""
ECE Department Course Registration System - Core Models
Contains Course, Student, and RegistrationSystem classes
"""

from typing import List, Dict, Tuple, Optional
from database import Database


class Course:
    """
    Course class representing a single course
    
    Attributes:
        course_code: Unique course identifier
        name: Course name
        credits: Number of credits
        lecture_hours: Weekly lecture hours
        lab_hours: Weekly lab hours
        max_capacity: Maximum number of students
        prerequisites: List of prerequisite course codes
    """
    
    def __init__(self, course_code: str, name: str, credits: int, 
                 lecture_hours: int, lab_hours: int, max_capacity: int,
                 prerequisites: List[str] = None, description: str = ""):
        self.course_code = course_code
        self.name = name
        self.credits = credits
        self.lecture_hours = lecture_hours
        self.lab_hours = lab_hours
        self.max_capacity = max_capacity
        self.prerequisites = prerequisites or []
        self.description = description
        self.id = None  # Database ID, set after insertion
    
    def check_prerequisites(self, student_transcript: List[Dict]) -> Tuple[bool, List[str]]:
        """
        Check if student has completed all prerequisites
        
        Args:
            student_transcript: List of completed courses
            
        Returns:
            Tuple of (prerequisites_met: bool, missing_prerequisites: List[str])
        """
        if not self.prerequisites:
            return True, []
        
        completed_codes = {course['course_code'] for course in student_transcript if course.get('passed', False)}
        missing = [prereq for prereq in self.prerequisites if prereq not in completed_codes]
        
        return len(missing) == 0, missing
    
    def is_full(self, current_enrollment: int) -> bool:
        """
        Check if course has reached maximum capacity
        
        Args:
            current_enrollment: Current number of enrolled students
            
        Returns:
            True if course is full, False otherwise
        """
        return current_enrollment >= self.max_capacity
    
    def __str__(self):
        return f"{self.course_code} - {self.name} ({self.credits} credits)"
    
    def __repr__(self):
        return f"Course({self.course_code}, {self.name})"


class Student:
    """
    Student class representing a student
    
    Attributes:
        student_id: Unique student identifier
        name: Student name
        email: Student email
        program: ECE program (Computer, Communications, Power, Biomedical)
        level: Current academic level (1-4)
        transcript: List of completed courses with grades
    """
    
    def __init__(self, student_id: str, name: str, email: str, 
                 program: str, level: int, transcript: List[Dict] = None):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.level = level
        self.transcript = transcript or []
        self.id = None  # Database ID, set after insertion
    
    def get_completed_credits(self) -> int:
        """
        Calculate total completed credits
        
        Returns:
            Total number of credits from passed courses
        """
        return sum(course['credits'] for course in self.transcript if course.get('passed', False))
    
    def add_to_transcript(self, course: Dict, grade: str, passed: bool):
        """
        Add a course to the student's transcript
        
        Args:
            course: Course dictionary
            grade: Grade received
            passed: Whether the student passed
        """
        transcript_entry = {
            **course,
            'grade': grade,
            'passed': passed
        }
        self.transcript.append(transcript_entry)
    
    def has_completed_course(self, course_code: str) -> bool:
        """
        Check if student has completed a specific course
        
        Args:
            course_code: Course code to check
            
        Returns:
            True if completed and passed, False otherwise
        """
        for course in self.transcript:
            if course['course_code'] == course_code and course.get('passed', False):
                return True
        return False
    
    def get_gpa(self) -> float:
        """
        Calculate student's GPA (simplified)
        A=4.0, B=3.0, C=2.0, D=1.0, F=0.0
        
        Returns:
            GPA as float
        """
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        total_points = 0.0
        total_credits = 0
        
        for course in self.transcript:
            if course.get('passed', False) and course.get('grade'):
                grade = course['grade'][0] if course['grade'] else 'F'  # Take first letter
                points = grade_points.get(grade, 0.0)
                credits = course.get('credits', 0)
                total_points += points * credits
                total_credits += credits
        
        return total_points / total_credits if total_credits > 0 else 0.0
    
    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.program})"
    
    def __repr__(self):
        return f"Student({self.student_id}, {self.name})"


class RegistrationSystem:
    """
    Registration System class handling all registration operations
    Manages database connections and course validation logic
    """
    
    def __init__(self):
        """Initialize the registration system with database connection"""
        self.db = Database()
    
    def validate_schedule(self, student: Student, selected_courses: List[Dict], 
                         semester_year: str) -> Tuple[bool, List[str]]:
        """
        Validate a student's course selection against all constraints
        
        Args:
            student: Student object
            selected_courses: List of selected course dictionaries
            semester_year: Current semester/year
            
        Returns:
            Tuple of (is_valid: bool, error_messages: List[str])
        """
        errors = []
        
        # 1. Check credit hour limits (12-18 credits)
        total_credits = sum(course['credits'] for course in selected_courses)
        if total_credits < 12:
            errors.append(f"Total credits ({total_credits}) is below minimum of 12")
        elif total_credits > 18:
            errors.append(f"Total credits ({total_credits}) exceeds maximum of 18")
        
        # 2. Check prerequisites for each course
        for course in selected_courses:
            prereqs = self.db.get_course_prerequisites(course['id'])
            if prereqs:
                missing_prereqs = []
                for prereq in prereqs:
                    if not student.has_completed_course(prereq['course_code']):
                        missing_prereqs.append(prereq['course_code'])
                
                if missing_prereqs:
                    errors.append(
                        f"Cannot register for {course['course_code']}: "
                        f"Missing prerequisites: {', '.join(missing_prereqs)}"
                    )
        
        # 3. Check course capacity
        for course in selected_courses:
            enrollment = self.db.get_course_enrollment_count(course['id'], semester_year)
            if enrollment >= course['max_capacity']:
                errors.append(f"Course {course['course_code']} is full ({enrollment}/{course['max_capacity']})")
        
        # 4. Check for schedule conflicts
        schedule_conflicts = self._check_schedule_conflicts(selected_courses, semester_year)
        errors.extend(schedule_conflicts)
        
        # 5. Check program plan adherence
        plan_errors = self._check_program_plan(student, selected_courses)
        errors.extend(plan_errors)
        
        return len(errors) == 0, errors
    
    def _check_schedule_conflicts(self, courses: List[Dict], semester_year: str) -> List[str]:
        """
        Check for time conflicts between courses
        
        Args:
            courses: List of course dictionaries
            semester_year: Current semester/year
            
        Returns:
            List of conflict error messages
        """
        errors = []
        schedules = []
        
        # Gather all schedules
        for course in courses:
            course_schedules = self.db.get_course_schedule(course['id'], semester_year)
            for sched in course_schedules:
                schedules.append({
                    'course': course,
                    'schedule': sched
                })
        
        # Check for overlaps
        for i, entry1 in enumerate(schedules):
            for entry2 in schedules[i+1:]:
                if self._schedules_overlap(entry1['schedule'], entry2['schedule']):
                    errors.append(
                        f"Schedule conflict: {entry1['course']['course_code']} "
                        f"{'Lab' if entry1['schedule']['is_lab'] else 'Lecture'} "
                        f"overlaps with {entry2['course']['course_code']} "
                        f"{'Lab' if entry2['schedule']['is_lab'] else 'Lecture'} "
                        f"on {entry1['schedule']['day']}"
                    )
        
        return errors
    
    def _schedules_overlap(self, sched1: Dict, sched2: Dict) -> bool:
        """Check if two schedules overlap"""
        if sched1['day'] != sched2['day']:
            return False
        
        # Convert times to comparable format
        start1 = self._time_to_minutes(sched1['start_time'])
        end1 = self._time_to_minutes(sched1['end_time'])
        start2 = self._time_to_minutes(sched2['start_time'])
        end2 = self._time_to_minutes(sched2['end_time'])
        
        # Check overlap
        return not (end1 <= start2 or end2 <= start1)
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert time string (HH:MM) to minutes since midnight"""
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except:
            return 0
    
    def _check_program_plan(self, student: Student, courses: List[Dict]) -> List[str]:
        """
        Check if courses are part of student's program plan
        
        Args:
            student: Student object
            courses: List of course dictionaries
            
        Returns:
            List of warning messages (not blocking)
        """
        warnings = []
        
        # Get program plan for student's level
        for semester in [1, 2]:  # Check both semesters
            plan_courses = self.db.get_program_plan_courses(student.program, student.level, semester)
            plan_codes = {c['course_code'] for c in plan_courses}
            
            for course in courses:
                if course['course_code'] not in plan_codes:
                    # Check if it's in other programs (might be elective)
                    warnings.append(
                        f"Warning: {course['course_code']} is not in the standard "
                        f"{student.program} program plan for Level {student.level}"
                    )
        
        return warnings
    
    def register_student(self, student: Student, course_list: List[Dict], 
                        semester_year: str) -> Tuple[bool, str]:
        """
        Register a student for a list of courses after validation
        
        Args:
            student: Student object
            course_list: List of course dictionaries
            semester_year: Current semester/year
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate the schedule
        is_valid, errors = self.validate_schedule(student, course_list, semester_year)
        
        if not is_valid:
            return False, "Registration failed:\n" + "\n".join(errors)
        
        # Register for each course
        success_count = 0
        for course in course_list:
            success, msg = self.db.register_student_for_course(
                student.id, course['id'], semester_year
            )
            if success:
                success_count += 1
        
        if success_count == len(course_list):
            return True, f"Successfully registered for {success_count} courses"
        else:
            return False, f"Registered for {success_count}/{len(course_list)} courses"
    
    def add_course(self, course: Course) -> Tuple[bool, str]:
        """
        Add a new course to the system
        
        Args:
            course: Course object
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        return self.db.add_course(
            course.course_code, course.name, course.credits,
            course.lecture_hours, course.lab_hours, course.max_capacity,
            course.description
        )
    
    def get_available_courses(self, program: str, level: int, semester: int) -> List[Dict]:
        """
        Get available courses for a specific program and level
        
        Args:
            program: ECE program
            level: Academic level
            semester: Semester (1 or 2)
            
        Returns:
            List of available courses
        """
        return self.db.get_program_plan_courses(program, level, semester)
    
    def get_student_info(self, student_id: int) -> Optional[Student]:
        """
        Get complete student information including transcript
        
        Args:
            student_id: Database student ID
            
        Returns:
            Student object or None
        """
        student_data = self.db.get_student_by_id(student_id)
        if not student_data:
            return None
        
        transcript = self.db.get_student_transcript(student_id)
        
        return Student(
            student_id=student_data['student_id'],
            name=student_data['name'],
            email=student_data['email'],
            program=student_data['program'],
            level=student_data['level'],
            transcript=transcript
        )

