"""Tests for Lab 10 — School Management System (Mini Project, Intermediate Capstone).

Definitions mirror the notebook cells exactly. Covers:
- TestPerson        : attributes, __str__/__repr__
- TestStudent       : inheritance, encapsulation, property validation, role_info
- TestTeacher       : inheritance, role_info
- TestPolymorphism  : same method name -> different behaviour
- TestClassroom     : inner class, subject, mixed roster
- TestSchool        : add_classroom/add_member, __len__, report
- TestIntegration   : end-to-end scenario
"""
import pytest


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def role_info(self):
        return f"Base person {self.name}, age {self.age}"

    def __str__(self):
        return f"{self.name} (age {self.age})"

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


class Student(Person):
    def __init__(self, name, age, course, marks):
        super().__init__(name, age)
        self.course = course
        self._marks = marks

    @property
    def marks(self):
        return self._marks

    @marks.setter
    def marks(self, value):
        if value < 0 or value > 100:
            raise ValueError("Marks must be between 0 and 100")
        self._marks = value

    def role_info(self):
        return f"Student {self.name} takes {self.course} and scored {self.marks}"

    def __str__(self):
        return f"{self.name} ({self.course})"


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def role_info(self):
        return f"Teacher {self.name} teaches {self.subject}"


class School:
    total_members = 0

    def __init__(self, name):
        self.name = name
        self.classrooms = []

    @classmethod
    def increment_members(cls):
        cls.total_members += 1

    class Classroom:
        def __init__(self, parent, subject):
            self.parent = parent
            self.subject = subject
            self.roster = []

        def add_member(self, person):
            self.roster.append(person)
            School.increment_members()

        def __len__(self):
            return len(self.roster)

        def __str__(self):
            return f"{self.subject} ({len(self.roster)} members)"

    def add_classroom(self, subject):
        room = self.Classroom(self, subject)
        self.classrooms.append(room)
        return room

    def add_member(self, person, classroom):
        classroom.add_member(person)

    def __len__(self):
        return sum(len(c) for c in self.classrooms)

    def __str__(self):
        lines = [f"{self.name} School ({len(self)} members)"]
        for c in self.classrooms:
            names = ", ".join(str(p) for p in c.roster)
            lines.append(f"  {c.subject}: {names}")
        return "\n".join(lines)


class TestPerson:
    def test_attributes_set(self):
        p = Person("Ada", 30)
        assert p.name == "Ada"
        assert p.age == 30

    def test_str_output(self):
        p = Person("Ada", 30)
        assert str(p) == "Ada (age 30)"

    def test_repr_output(self):
        p = Person("Ada", 30)
        assert repr(p) == "Person('Ada', 30)"

    def test_base_role_info(self):
        p = Person("Ada", 30)
        assert p.role_info() == "Base person Ada, age 30"


class TestStudent:
    def test_inherits_person(self):
        s = Student("Ana", 15, "Math", 88)
        assert isinstance(s, Person)
        assert s.name == "Ana"
        assert s.age == 15

    def test_private_marks_stored(self):
        s = Student("Ana", 15, "Math", 88)
        assert s._marks == 88

    def test_property_reads_marks(self):
        s = Student("Ana", 15, "Math", 88)
        assert s.marks == 88

    def test_property_validates_negative(self):
        s = Student("Ana", 15, "Math", 88)
        with pytest.raises(ValueError):
            s.marks = -5

    def test_property_validates_over_100(self):
        s = Student("Ana", 15, "Math", 88)
        with pytest.raises(ValueError):
            s.marks = 150

    def test_property_zero_and_hundred_allowed(self):
        s = Student("Ana", 15, "Math", 88)
        s.marks = 0
        assert s.marks == 0
        s.marks = 100
        assert s.marks == 100

    def test_role_info_shows_course_and_marks(self):
        s = Student("Ana", 15, "Math", 88)
        assert s.role_info() == "Student Ana takes Math and scored 88"

    def test_str_overridden(self):
        s = Student("Ana", 15, "Math", 88)
        assert str(s) == "Ana (Math)"


class TestTeacher:
    def test_inherits_person(self):
        t = Teacher("Mr. Bell", 38, "Math")
        assert isinstance(t, Person)
        assert t.name == "Mr. Bell"
        assert t.age == 38

    def test_has_subject(self):
        t = Teacher("Mr. Bell", 38, "Math")
        assert t.subject == "Math"

    def test_role_info_shows_subject(self):
        t = Teacher("Mr. Bell", 38, "Math")
        assert t.role_info() == "Teacher Mr. Bell teaches Math"

    def test_role_info_distinct_from_student(self):
        t = Teacher("Mr. Bell", 38, "Math")
        s = Student("Ana", 15, "Math", 88)
        assert t.role_info() != s.role_info()


class TestPolymorphism:
    def test_same_name_student_text(self):
        s = Student("Leo", 16, "Physics", 92)
        assert "Student" in s.role_info()

    def test_same_name_teacher_text(self):
        t = Teacher("Ms. Ruiz", 45, "Physics")
        assert "Teacher" in t.role_info()

    def test_loop_invokes_correct_version(self):
        people = [
            Student("Ana", 15, "Math", 88),
            Student("Leo", 16, "Physics", 92),
            Teacher("Mr. Bell", 38, "Math"),
            Teacher("Ms. Ruiz", 45, "Physics"),
        ]
        results = [p.role_info() for p in people]
        assert results[0] == "Student Ana takes Math and scored 88"
        assert results[1] == "Student Leo takes Physics and scored 92"
        assert results[2] == "Teacher Mr. Bell teaches Math"
        assert results[3] == "Teacher Ms. Ruiz teaches Physics"


class TestClassroom:
    def test_created_through_school(self):
        school = School("Sunrise High")
        room = school.add_classroom("Math")
        assert isinstance(room, School.Classroom)

    def test_has_subject(self):
        school = School("Sunrise High")
        room = school.add_classroom("Math")
        assert room.subject == "Math"

    def test_roster_holds_mixed_person_types(self):
        school = School("Sunrise High")
        room = school.add_classroom("Math")
        room.add_member(Student("Ana", 15, "Math", 88))
        room.add_member(Teacher("Mr. Bell", 38, "Math"))
        assert isinstance(room.roster[0], Student)
        assert isinstance(room.roster[1], Teacher)

    def test_len_room(self):
        school = School("Sunrise High")
        room = school.add_classroom("Math")
        room.add_member(Student("Ana", 15, "Math", 88))
        room.add_member(Teacher("Mr. Bell", 38, "Math"))
        assert len(room) == 2


class TestSchool:
    def test_add_classroom_works(self):
        school = School("Sunrise High")
        room = school.add_classroom("Physics")
        assert room.subject == "Physics"
        assert school.classrooms == [room]

    def test_add_member_works(self):
        school = School("Sunrise High")
        room = school.add_classroom("Math")
        school.add_member(Student("Ana", 15, "Math", 88), room)
        assert len(room.roster) == 1

    def test_len_returns_total_members(self):
        school = School("Sunrise High")
        math = school.add_classroom("Math")
        physics = school.add_classroom("Physics")
        math.add_member(Student("Ana", 15, "Math", 88))
        math.add_member(Teacher("Mr. Bell", 38, "Math"))
        physics.add_member(Student("Leo", 16, "Physics", 92))
        assert len(school) == 3

    def test_report_prints_all(self, capsys):
        school = School("Sunrise High")
        math = school.add_classroom("Math")
        math.add_member(Student("Ana", 15, "Math", 88))
        math.add_member(Teacher("Mr. Bell", 38, "Math"))
        print(school)
        captured = capsys.readouterr().out
        assert "Sunrise High School (2 members)" in captured
        assert "Ana (Math)" in captured
        assert "Mr. Bell (age 38)" in captured


class TestIntegration:
    def test_end_to_end_scenario(self, capsys):
        School.total_members = 0
        school = School("Sunrise High")
        math = school.add_classroom("Math")
        physics = school.add_classroom("Physics")

        math.add_member(Student("Ana", 15, "Math", 88))
        math.add_member(Student("Ben", 14, "Math", 72))
        math.add_member(Teacher("Mr. Bell", 38, "Math"))
        physics.add_member(Student("Leo", 16, "Physics", 92))
        physics.add_member(Student("Mia", 15, "Physics", 81))
        physics.add_member(Teacher("Ms. Ruiz", 45, "Physics"))

        assert len(school) == 6
        assert School.total_members == 6
        assert len(school.classrooms) == 2

        print(school)
        captured = capsys.readouterr().out
        assert "Sunrise High School (6 members)" in captured
        assert "Math: Ana (Math), Ben (Math), Mr. Bell (age 38)" in captured
        assert "Physics: Leo (Physics), Mia (Physics), Ms. Ruiz (age 45)" in captured

        reports = [p.role_info() for p in math.roster]
        assert reports[0] == "Student Ana takes Math and scored 88"
        assert reports[2] == "Teacher Mr. Bell teaches Math"
