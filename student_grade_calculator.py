#Demitree Hebert
#CIS261
#WK10 VIBE Coding

"""
Student Grade Calculator
Manages student records, calculates grades, and provides class statistics.
"""

import os
import sys
from typing import List, Optional


class Student:
    """Represents a student with grades and calculated average/letter grade."""
    
    def __init__(self, name: str, student_id: str, test1: float, test2: float, test3: float):
        """Initialize a student with name, ID, and three test scores."""
        self.name = name
        self.student_id = student_id
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()
    
    def calculate_average(self) -> float:
        """Calculate the average of the three test scores."""
        return (self.test1 + self.test2 + self.test3) / 3
    
    def calculate_grade(self) -> str:
        """Calculate letter grade based on average score."""
        if self.average >= 90:
            return 'A'
        elif self.average >= 80:
            return 'B'
        elif self.average >= 70:
            return 'C'
        elif self.average >= 60:
            return 'D'
        else:
            return 'F'
    
    def to_file_format(self) -> str:
        """Convert student data to pipe-delimited format for file storage."""
        return f"{self.name}|{self.student_id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"
    
    @staticmethod
    def from_file_format(line: str) -> 'Student':
        """Create a Student object from a pipe-delimited string."""
        parts = line.strip().split('|')
        if len(parts) != 7:
            raise ValueError(f"Invalid file format: {line}")
        name, student_id, test1, test2, test3, _, _ = parts
        return Student(name, student_id, float(test1), float(test2), float(test3))


class StudentGradeManager:
    """Manages a collection of students and file operations."""
    
    def __init__(self, filename: str = "student_grades.txt"):
        """Initialize the manager with a filename for persistence."""
        self.filename = filename
        self.students: List[Student] = []
        self.load_students()
    
    def add_student(self, name: str, student_id: str, test1: float, test2: float, test3: float) -> None:
        """Add a new student to the list."""
        student = Student(name, student_id, test1, test2, test3)
        self.students.append(student)
    
    def save_students(self) -> None:
        """Save all student records to file."""
        try:
            with open(self.filename, 'w') as f:
                for student in self.students:
                    f.write(student.to_file_format() + '\n')
            print(f"\n✓ Records saved successfully to {self.filename}")
        except IOError as e:
            print(f"\n✗ Error saving file: {e}")
    
    def load_students(self) -> None:
        """Load student records from file if it exists."""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            student = Student.from_file_format(line)
                            self.students.append(student)
                        except ValueError as e:
                            print(f"Warning: Skipping invalid record: {e}")
            if self.students:
                print(f"✓ Loaded {len(self.students)} student(s) from {self.filename}\n")
        except IOError as e:
            print(f"Warning: Could not load file: {e}\n")
    
    def display_all_students(self) -> None:
        """Display all students in a formatted table."""
        if not self.students:
            print("\nNo students in the system.\n")
            return
        
        print("\n" + "="*100)
        print(f"{'Name':<20} {'Student ID':<15} {'Test 1':<10} {'Test 2':<10} {'Test 3':<10} {'Average':<10} {'Grade':<10}")
        print("="*100)
        
        for student in self.students:
            print(f"{student.name:<20} {student.student_id:<15} {student.test1:<10.2f} {student.test2:<10.2f} {student.test3:<10.2f} {student.average:<10.2f} {student.grade:<10}")
        
        print("="*100 + "\n")
    
    def calculate_class_statistics(self) -> None:
        """Display class statistics."""
        if not self.students:
            print("\nNo students to calculate statistics.\n")
            return
        
        averages = [student.average for student in self.students]
        highest = max(averages)
        lowest = min(averages)
        class_average = sum(averages) / len(averages)
        
        # Find students with highest and lowest averages
        highest_student = next(student for student in self.students if student.average == highest)
        lowest_student = next(student for student in self.students if student.average == lowest)
        
        print("\n" + "="*50)
        print("CLASS STATISTICS")
        print("="*50)
        print(f"Number of Students:    {len(self.students)}")
        print(f"Class Average:         {class_average:.2f}")
        print(f"Highest Average:       {highest:.2f} ({highest_student.name})")
        print(f"Lowest Average:        {lowest:.2f} ({lowest_student.name})")
        print("="*50 + "\n")
    
    def search_student_by_name(self, name: str) -> Optional[Student]:
        """Search for a student by name (case-insensitive)."""
        name_lower = name.lower()
        for student in self.students:
            if student.name.lower() == name_lower:
                return student
        return None
    
    def display_search_result(self, name: str) -> None:
        """Display search result for a student."""
        student = self.search_student_by_name(name)
        if student:
            print("\n" + "="*70)
            print(f"Name:          {student.name}")
            print(f"Student ID:    {student.student_id}")
            print(f"Test 1:        {student.test1:.2f}")
            print(f"Test 2:        {student.test2:.2f}")
            print(f"Test 3:        {student.test3:.2f}")
            print(f"Average:       {student.average:.2f}")
            print(f"Grade:         {student.grade}")
            print("="*70 + "\n")
        else:
            print(f"\n✗ Student '{name}' not found.\n")


def get_float_input(prompt: str) -> float:
    """Get a valid float input from the user."""
    while True:
        try:
            value = float(input(prompt))
            if not (0 <= value <= 100):
                print("Please enter a score between 0 and 100.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def add_student_menu(manager: StudentGradeManager) -> None:
    """Handle adding a new student."""
    print("\n" + "="*50)
    print("ADD NEW STUDENT")
    print("="*50)
    
    name = input("Enter student name: ").strip()
    if not name:
        print("✗ Name cannot be empty.")
        return
    
    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("✗ Student ID cannot be empty.")
        return
    
    test1 = get_float_input("Enter Test 1 score (0-100): ")
    test2 = get_float_input("Enter Test 2 score (0-100): ")
    test3 = get_float_input("Enter Test 3 score (0-100): ")
    
    manager.add_student(name, student_id, test1, test2, test3)
    print(f"\n✓ Student '{name}' added successfully.")


def main_menu(manager: StudentGradeManager) -> bool:
    """Display main menu and handle user choice. Returns False if user exits."""
    print("\n" + "="*50)
    print("STUDENT GRADE CALCULATOR")
    print("="*50)
    print("1. Add new student")
    print("2. Display all students")
    print("3. View class statistics")
    print("4. Search for a student")
    print("5. Save and exit (ESC)")
    print("="*50)
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == '1':
        add_student_menu(manager)
        return True
    elif choice == '2':
        manager.display_all_students()
        return True
    elif choice == '3':
        manager.calculate_class_statistics()
        return True
    elif choice == '4':
        name = input("\nEnter student name to search: ").strip()
        manager.display_search_result(name)
        return True
    elif choice == '5':
        manager.save_students()
        print("Thank you for using Student Grade Calculator. Goodbye!")
        return False
    else:
        print("✗ Invalid choice. Please try again.")
        return True


def main():
    """Main program entry point."""
    print("\n" + "="*50)
    print("Welcome to Student Grade Calculator!")
    print("="*50)
    
    manager = StudentGradeManager()
    
    while True:
        try:
            if not main_menu(manager):
                break
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Saving records...")
            manager.save_students()
            print("Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ An error occurred: {e}")


if __name__ == "__main__":
    main()
