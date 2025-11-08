"""
Course Registration System - Main Application
A simple GUI-based course registration system using tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database import Database, Student, Course


class CourseRegistrationApp:
    """Main application class for Course Registration System"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Course Registration System")
        self.root.geometry("1000x600")
        
        # Initialize database
        self.db = Database()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Create tabs
        self.create_students_tab()
        self.create_courses_tab()
        self.create_registration_tab()
        
    def create_header(self):
        """Create application header"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            header_frame, 
            text="Course Registration System", 
            font=('Arial', 20, 'bold')
        )
        title_label.pack(pady=10)
    
    def create_students_tab(self):
        """Create the students management tab"""
        students_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(students_frame, text="Students")
        
        # Configure grid
        students_frame.columnconfigure(0, weight=1)
        students_frame.rowconfigure(1, weight=1)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(students_frame, text="Student Management", padding="10")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Input fields
        ttk.Label(controls_frame, text="Student ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.student_id_entry = ttk.Entry(controls_frame, width=20)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(controls_frame, text="Name:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0), pady=2)
        self.student_name_entry = ttk.Entry(controls_frame, width=25)
        self.student_name_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(controls_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.student_email_entry = ttk.Entry(controls_frame, width=20)
        self.student_email_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(controls_frame, text="Major:").grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=2)
        self.student_major_entry = ttk.Entry(controls_frame, width=25)
        self.student_major_entry.grid(row=1, column=3, padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_students).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(controls_frame)
        search_frame.grid(row=3, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.student_search_entry = ttk.Entry(search_frame, width=30)
        self.student_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_students).pack(side=tk.LEFT, padx=5)
        
        # Students list
        list_frame = ttk.Frame(students_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ('ID', 'Student ID', 'Name', 'Email', 'Major')
        self.students_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.students_tree.yview)
        self.students_tree.configure(yscroll=scrollbar.set)
        
        self.students_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click to view registrations
        self.students_tree.bind('<Double-Button-1>', self.view_student_registrations)
        
        # Load initial data
        self.refresh_students()
    
    def create_courses_tab(self):
        """Create the courses management tab"""
        courses_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(courses_frame, text="Courses")
        
        # Configure grid
        courses_frame.columnconfigure(0, weight=1)
        courses_frame.rowconfigure(1, weight=1)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(courses_frame, text="Course Management", padding="10")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Input fields
        ttk.Label(controls_frame, text="Course Code:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.course_code_entry = ttk.Entry(controls_frame, width=15)
        self.course_code_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(controls_frame, text="Name:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0), pady=2)
        self.course_name_entry = ttk.Entry(controls_frame, width=30)
        self.course_name_entry.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(controls_frame, text="Instructor:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.course_instructor_entry = ttk.Entry(controls_frame, width=15)
        self.course_instructor_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(controls_frame, text="Credits:").grid(row=1, column=2, sticky=tk.W, padx=(10, 0), pady=2)
        self.course_credits_entry = ttk.Entry(controls_frame, width=10)
        self.course_credits_entry.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(controls_frame, text="Max Students:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.course_max_entry = ttk.Entry(controls_frame, width=10)
        self.course_max_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Add Course", command=self.add_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_courses).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(controls_frame)
        search_frame.grid(row=4, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.course_search_entry = ttk.Entry(search_frame, width=30)
        self.course_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_courses).pack(side=tk.LEFT, padx=5)
        
        # Courses list
        list_frame = ttk.Frame(courses_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ('ID', 'Code', 'Name', 'Instructor', 'Credits', 'Max Students')
        self.courses_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.courses_tree.heading(col, text=col)
            if col == 'Name':
                self.courses_tree.column(col, width=250)
            else:
                self.courses_tree.column(col, width=120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.courses_tree.yview)
        self.courses_tree.configure(yscroll=scrollbar.set)
        
        self.courses_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double-click to view registrations
        self.courses_tree.bind('<Double-Button-1>', self.view_course_registrations)
        
        # Load initial data
        self.refresh_courses()
    
    def create_registration_tab(self):
        """Create the registration management tab"""
        reg_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(reg_frame, text="Register for Course")
        
        # Configure grid
        reg_frame.columnconfigure(0, weight=1)
        reg_frame.rowconfigure(2, weight=1)
        
        # Instructions
        instructions = ttk.Label(
            reg_frame, 
            text="Select a student and a course, then click 'Register' to enroll the student in the course.",
            wraplength=900
        )
        instructions.grid(row=0, column=0, pady=(0, 10))
        
        # Selection frame
        selection_frame = ttk.LabelFrame(reg_frame, text="Registration Details", padding="10")
        selection_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Student selection
        ttk.Label(selection_frame, text="Select Student:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_student_combo = ttk.Combobox(selection_frame, width=40, state='readonly')
        self.reg_student_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Course selection
        ttk.Label(selection_frame, text="Select Course:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_course_combo = ttk.Combobox(selection_frame, width=40, state='readonly')
        self.reg_course_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Semester input
        ttk.Label(selection_frame, text="Semester:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_semester_entry = ttk.Entry(selection_frame, width=20)
        self.reg_semester_entry.insert(0, "Fall 2024")
        self.reg_semester_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(selection_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Register", command=self.register_student_for_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh Lists", command=self.refresh_registration_combos).pack(side=tk.LEFT, padx=5)
        
        # All registrations list
        list_label = ttk.Label(reg_frame, text="All Registrations", font=('Arial', 12, 'bold'))
        list_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        list_frame = ttk.Frame(reg_frame)
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview for all registrations
        columns = ('Reg ID', 'Student ID', 'Student Name', 'Course Code', 'Course Name', 'Semester', 'Grade')
        self.registrations_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.registrations_tree.heading(col, text=col)
            if col in ['Student Name', 'Course Name']:
                self.registrations_tree.column(col, width=200)
            else:
                self.registrations_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.registrations_tree.yview)
        self.registrations_tree.configure(yscroll=scrollbar.set)
        
        self.registrations_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Context menu for registrations
        self.reg_menu = tk.Menu(self.registrations_tree, tearoff=0)
        self.reg_menu.add_command(label="Drop Registration", command=self.drop_registration)
        self.reg_menu.add_command(label="Update Grade", command=self.update_grade)
        
        self.registrations_tree.bind("<Button-3>", self.show_registration_context_menu)
        
        # Load initial data
        self.refresh_registration_combos()
        self.refresh_all_registrations()
    
    # Student operations
    def add_student(self):
        """Add a new student"""
        student_id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        email = self.student_email_entry.get().strip()
        major = self.student_major_entry.get().strip()
        
        if not all([student_id, name, email, major]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        student = Student(student_id=student_id, name=name, email=email, major=major)
        
        if self.db.add_student(student):
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_student_entries()
            self.refresh_students()
        else:
            messagebox.showerror("Error", "Student ID already exists!")
    
    def delete_student(self):
        """Delete selected student"""
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete!")
            return
        
        student_id = self.students_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            if self.db.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Failed to delete student!")
    
    def refresh_students(self):
        """Refresh students list"""
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        students = self.db.get_all_students()
        for student in students:
            self.students_tree.insert('', tk.END, values=(
                student.id, student.student_id, student.name, 
                student.email, student.major
            ))
    
    def search_students(self):
        """Search students"""
        search_term = self.student_search_entry.get().strip()
        
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        if search_term:
            students = self.db.search_students(search_term)
        else:
            students = self.db.get_all_students()
        
        for student in students:
            self.students_tree.insert('', tk.END, values=(
                student.id, student.student_id, student.name, 
                student.email, student.major
            ))
    
    def clear_student_entries(self):
        """Clear student input fields"""
        self.student_id_entry.delete(0, tk.END)
        self.student_name_entry.delete(0, tk.END)
        self.student_email_entry.delete(0, tk.END)
        self.student_major_entry.delete(0, tk.END)
    
    # Course operations
    def add_course(self):
        """Add a new course"""
        code = self.course_code_entry.get().strip()
        name = self.course_name_entry.get().strip()
        instructor = self.course_instructor_entry.get().strip()
        credits = self.course_credits_entry.get().strip()
        max_students = self.course_max_entry.get().strip()
        
        if not all([code, name, instructor, credits, max_students]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            credits = int(credits)
            max_students = int(max_students)
        except ValueError:
            messagebox.showerror("Error", "Credits and Max Students must be numbers!")
            return
        
        course = Course(
            course_code=code, name=name, instructor=instructor,
            credits=credits, max_students=max_students
        )
        
        if self.db.add_course(course):
            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_course_entries()
            self.refresh_courses()
        else:
            messagebox.showerror("Error", "Course code already exists!")
    
    def delete_course(self):
        """Delete selected course"""
        selected = self.courses_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a course to delete!")
            return
        
        course_id = self.courses_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this course?"):
            if self.db.delete_course(course_id):
                messagebox.showinfo("Success", "Course deleted successfully!")
                self.refresh_courses()
            else:
                messagebox.showerror("Error", "Failed to delete course!")
    
    def refresh_courses(self):
        """Refresh courses list"""
        for item in self.courses_tree.get_children():
            self.courses_tree.delete(item)
        
        courses = self.db.get_all_courses()
        for course in courses:
            self.courses_tree.insert('', tk.END, values=(
                course.id, course.course_code, course.name,
                course.instructor, course.credits, course.max_students
            ))
    
    def search_courses(self):
        """Search courses"""
        search_term = self.course_search_entry.get().strip()
        
        for item in self.courses_tree.get_children():
            self.courses_tree.delete(item)
        
        if search_term:
            courses = self.db.search_courses(search_term)
        else:
            courses = self.db.get_all_courses()
        
        for course in courses:
            self.courses_tree.insert('', tk.END, values=(
                course.id, course.course_code, course.name,
                course.instructor, course.credits, course.max_students
            ))
    
    def clear_course_entries(self):
        """Clear course input fields"""
        self.course_code_entry.delete(0, tk.END)
        self.course_name_entry.delete(0, tk.END)
        self.course_instructor_entry.delete(0, tk.END)
        self.course_credits_entry.delete(0, tk.END)
        self.course_max_entry.delete(0, tk.END)
    
    # Registration operations
    def refresh_registration_combos(self):
        """Refresh student and course combo boxes"""
        # Refresh students
        students = self.db.get_all_students()
        student_list = [f"{s.student_id} - {s.name}" for s in students]
        self.reg_student_combo['values'] = student_list
        self.student_id_map = {f"{s.student_id} - {s.name}": s.id for s in students}
        
        # Refresh courses
        courses = self.db.get_all_courses()
        course_list = [f"{c.course_code} - {c.name}" for c in courses]
        self.reg_course_combo['values'] = course_list
        self.course_id_map = {f"{c.course_code} - {c.name}": c.id for c in courses}
    
    def register_student_for_course(self):
        """Register a student for a course"""
        student_selection = self.reg_student_combo.get()
        course_selection = self.reg_course_combo.get()
        semester = self.reg_semester_entry.get().strip()
        
        if not all([student_selection, course_selection, semester]):
            messagebox.showerror("Error", "Please select student, course, and enter semester!")
            return
        
        student_id = self.student_id_map.get(student_selection)
        course_id = self.course_id_map.get(course_selection)
        
        success, message = self.db.register_student(student_id, course_id, semester)
        
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_all_registrations()
        else:
            messagebox.showerror("Error", message)
    
    def refresh_all_registrations(self):
        """Refresh the registrations list"""
        for item in self.registrations_tree.get_children():
            self.registrations_tree.delete(item)
        
        # Get all students and courses for lookup
        students = {s.id: s for s in self.db.get_all_students()}
        courses = {c.id: c for c in self.db.get_all_courses()}
        
        # Get all registrations
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.student_id, r.course_id, r.semester, r.grade
            FROM registrations r
        """)
        registrations = cursor.fetchall()
        self.db.close()
        
        for reg in registrations:
            student = students.get(reg['student_id'])
            course = courses.get(reg['course_id'])
            
            if student and course:
                self.registrations_tree.insert('', tk.END, values=(
                    reg['id'],
                    student.student_id,
                    student.name,
                    course.course_code,
                    course.name,
                    reg['semester'],
                    reg['grade'] or ''
                ))
    
    def show_registration_context_menu(self, event):
        """Show context menu for registrations"""
        item = self.registrations_tree.identify_row(event.y)
        if item:
            self.registrations_tree.selection_set(item)
            self.reg_menu.post(event.x_root, event.y_root)
    
    def drop_registration(self):
        """Drop a course registration"""
        selected = self.registrations_tree.selection()
        if not selected:
            return
        
        reg_id = self.registrations_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to drop this registration?"):
            if self.db.drop_registration(reg_id):
                messagebox.showinfo("Success", "Registration dropped successfully!")
                self.refresh_all_registrations()
            else:
                messagebox.showerror("Error", "Failed to drop registration!")
    
    def update_grade(self):
        """Update grade for a registration"""
        selected = self.registrations_tree.selection()
        if not selected:
            return
        
        reg_id = self.registrations_tree.item(selected[0])['values'][0]
        
        # Create dialog for grade input
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Grade")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter Grade:", font=('Arial', 10)).pack(pady=20)
        
        grade_var = tk.StringVar()
        grade_entry = ttk.Entry(dialog, textvariable=grade_var, width=10)
        grade_entry.pack(pady=10)
        grade_entry.focus()
        
        def save_grade():
            grade = grade_var.get().strip()
            if grade:
                if self.db.update_grade(reg_id, grade):
                    messagebox.showinfo("Success", "Grade updated successfully!")
                    self.refresh_all_registrations()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update grade!")
        
        ttk.Button(dialog, text="Save", command=save_grade).pack(pady=10)
        
        # Bind Enter key
        grade_entry.bind('<Return>', lambda e: save_grade())
    
    def view_student_registrations(self, event):
        """View registrations for selected student"""
        selected = self.students_tree.selection()
        if not selected:
            return
        
        student_db_id = self.students_tree.item(selected[0])['values'][0]
        student_name = self.students_tree.item(selected[0])['values'][2]
        
        registrations = self.db.get_student_registrations(student_db_id)
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Registrations for {student_name}")
        dialog.geometry("700x400")
        
        # Create treeview
        columns = ('Course Code', 'Course Name', 'Instructor', 'Credits', 'Semester', 'Grade')
        tree = ttk.Treeview(dialog, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        
        for reg in registrations:
            tree.insert('', tk.END, values=(
                reg['course_code'], reg['name'], reg['instructor'],
                reg['credits'], reg['semester'], reg['grade'] or 'N/A'
            ))
        
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def view_course_registrations(self, event):
        """View registrations for selected course"""
        selected = self.courses_tree.selection()
        if not selected:
            return
        
        course_db_id = self.courses_tree.item(selected[0])['values'][0]
        course_name = self.courses_tree.item(selected[0])['values'][2]
        
        registrations = self.db.get_course_registrations(course_db_id)
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Students Enrolled in {course_name}")
        dialog.geometry("600x400")
        
        # Create treeview
        columns = ('Student ID', 'Name', 'Email', 'Semester', 'Grade')
        tree = ttk.Treeview(dialog, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=115)
        
        for reg in registrations:
            tree.insert('', tk.END, values=(
                reg['student_id'], reg['name'], reg['email'],
                reg['semester'], reg['grade'] or 'N/A'
            ))
        
        scrollbar = ttk.Scrollbar(dialog, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CourseRegistrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

