# Lab 10 Assignment: Mini Project — School Management System

This assignment tests what you learned in **Lab 10: Mini Project — School Management System**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab10_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-school-management-system.md) and [Section 10 (Step-wise Instructions)](lab-school-management-system.md).

## Concept Questions

**1.** What does `super().__init__(name, age)` do in the `Student` and `Teacher` constructors? Why must each subclass call it?

**2.** How does the `marks` property enforce encapsulation? What happens if code tries to assign `student.marks = 150` or `student.marks = -5`?

**3.** How is polymorphism demonstrated by the `role_info()` method? Why can a single loop call it on a list that mixes `Student` and `Teacher` objects?

**4.** What is the difference between a class attribute / class method (like `School.total_members` and `increment_members()`) and an instance attribute like `self.classrooms`?

## Short Code Tasks

**5.** Write code that creates a `Teacher` named `"Ms. Ruiz"` of age `45` teaching `"Physics"` and prints `role_info()`.

**6.** Write code that creates a `Student("Ana", 15, "Math", 88)`, reads `marks` through the property, and prints its `repr` and `str`.

**7.** Using the classes from the lab, write code that builds a `School("Sunrise High")`, adds a `"History"` classroom, adds one `Student` and one `Teacher` to it, and prints `len(school)`.

## Applied Tasks

**8.** Write a function `print_roster(people)` that takes a mixed list of `Student` and `Teacher` objects and prints each one's `role_info()`. Then call it with a list containing one of each and state the exact two lines it produces.

**9.** Extend the lab by giving `Teacher` a `__str__` that returns `f"{self.name} ({self.subject})"`. Explain how this changes the School report output compared to the default inherited `__str__`.

**10.** Explain, in 3–4 sentences, how this capstone ties together inheritance, encapsulation, polymorphism, inner classes, class methods, and dunder methods into one working system.

---

## Answer Key

**1.** `super().__init__(name, age)` calls the parent `Person` constructor, which sets the shared `name` and `age` attributes. Each subclass must call it so the base attributes are initialised exactly once, in one place, instead of being re-implemented in every subclass — reusing the parent's code (from Lab 8).

**2.** `_marks` is stored as a private-by-convention attribute. All reads go through the `marks` getter and all writes through the setter, which validates the value: `if value < 0 or value > 100: raise ValueError(...)`. Assigning `150` or `-5` raises a `ValueError` ("Marks must be between 0 and 100"), so a Student object can never hold invalid marks.

**3.** Both `Student` and `Teacher` override the `role_info()` method inherited from `Person`, each returning type-specific text. Because both are `Person` objects, a single `for p in people: print(p.role_info())` loop calls the same method name and each object dispatches to its own version automatically — that is polymorphism.

**4.** `School.total_members` is a **class attribute** shared by all instances; `increment_members()` is a **class method** that receives `cls` (the class) rather than `self`, and it updates the shared counter. In contrast, `self.classrooms` is an **instance attribute** — each `School` object has its own separate list of classrooms.

**5.**
```python
t = Teacher("Ms. Ruiz", 45, "Physics")
print(t.role_info())   # Teacher Ms. Ruiz teaches Physics
```

**6.**
```python
s = Student("Ana", 15, "Math", 88)
print(s.marks)         # 88
print(repr(s))         # Person('Ana', 15)   (inherited from Person)
print(str(s))          # Ana (Math)          (overridden in Student)
```

**7.**
```python
school = School("Sunrise High")
hist = school.add_classroom("History")
hist.add_member(Student("Nina", 14, "History", 85))
hist.add_member(Teacher("Dr. Okoye", 51, "History"))
print(len(school))     # 2
```

**8.**
```python
def print_roster(people):
    for p in people:
        print(p.role_info())

print_roster([Student("Ana", 15, "Math", 88), Teacher("Mr. Bell", 38, "Math")])
```
This produces exactly:
```
Student Ana takes Math and scored 88
Teacher Mr. Bell teaches Math
```

**9.**
```python
class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def role_info(self):
        return f"Teacher {self.name} teaches {self.subject}"

    def __str__(self):
        return f"{self.name} ({self.subject})"
```
With this override, `School.__str__` prints teachers as `Mr. Bell (Math)`
instead of the inherited `Mr. Bell (age 38)`. The change is contained to the
Teacher class, and the School report automatically reflects it — demonstrating
how `__str__` inheritance and override shape output.

**10.** The capstone starts with a `Person` base class and lets `Student` and `Teacher` **inherit** its shared state, calling `super().__init__`. Each subclass **overrides** `role_info()` (polymorphism), and `Student` additionally hides its marks behind a **validating property** (encapsulation). A `School` class contains an **inner** `Classroom` with a roster of mixed person types, uses a **classmethod** counter to track the total membership, and relies on **dunder methods** (`__len__`, `__str__`, `__repr__`) to give friendly printing and length behaviour. Together these pieces model a real organisation in one cohesive system.
