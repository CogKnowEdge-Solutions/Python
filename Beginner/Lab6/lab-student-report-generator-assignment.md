# Lab 6 Assignment: Mini Project — Student Report Generator

This assignment tests what you learned in **Lab 6: Mini Project — Student Report Generator**. You can answer each exercise from the lab alone — no need to re-run the notebook. Write and test any code tasks in a scratch file (`lab6_scratch.py`).

Reference sections: [Section 7 (Underlying Concepts)](lab-student-report-generator.md) and [Section 10 (Step-wise Instructions)](lab-student-report-generator.md).

## Concept Questions

**1.** What is the overall structure of the lab's gradebook, and how do you access a single student's course name?

**2.** Why is `build_report()` written as a separate function rather than inlined in the loop?

**3.** In the pipeline, describe what the `summaries` dict stores and which other tools it depends on.

**4.** What do the format specs `.1f`, `* 100:.0f`, and the `"\n".join(lines)` call each do in the formatting function?

## Short Code Tasks

**5.** Write code that, given the nested access pattern, prints `"Clara"`'s course name and her first score.

**6.** Write code that computes and prints the average of the list `[10, 20, 30]` using `sum()` and `len()`.

**7.** Write a `final_grade(average)` function that returns `"A"` for `average >= 90` and `"F"` otherwise. State what it returns for `final_grade(95)` and `final_grade(70)`.

## Applied Tasks

**8.** Using the lab's `student_data`, write a loop that prints, for each student, a line like `Ana (Data 101): 91.7`. (Hint: reuse `sum()` and `len()` and format with `.1f`.)

**9.** Extend **`build_report()`** to append an `"Honor Roll"` line when a student's grade is `"A"` and their attendance is `0.85` or higher. Write the modified function and state which of Ana, Ben, and Clara get the extra line.

**10.** Explain, in 2–3 sentences, how this mini project ties together variables, strings, a dictionary, conditional logic, and a formatting function into a single working program.

---

## Answer Key

**1.** The gradebook is a **dictionary of dictionaries**: the outer dict maps each student name to an inner dict with `course`, `scores`, and `attendance` keys. You access one student's course with `student_data["clara"]`'s key properly spelled — e.g. `student_data["Clara"]["course"]`.

**2.** `build_report()` is a separate function because it is called once per student (so it is reused, satisfying the "minimize but don't over-split" rule), and it isolates a single teachable idea — turning one record into a formatted string. Separating it keeps each step testable in its own cell and the loop clean.

**3.** `summaries` is a dict that maps each student name to a nested dict holding that student's `average` (a float) and `grade` (a letter). It depends on `student_data` (for scores), `sum()` and `len()` (to compute the average), and `final_grade()` (to convert the average to a letter).

**4.** `.1f` rounds the average to one decimal place. `* 100:.0f` multiplies the attendance ratio by 100 (turning `0.90` into `90`) and rounds to zero decimals, then the `%` writes a percent sign. `"\n".join(lines)` merges the list of strings into one multi-line string with newlines between them.

**5.**
```python
print(student_data["Clara"]["course"])
print(student_data["Clara"]["scores"][0])
```
This prints `Stats 210` and `55`.

**6.**
```python
numbers = [10, 20, 30]
average = sum(numbers) / len(numbers)
print(average)
```
This prints `20.0`.

**7.**
```python
def final_grade(average):
    if average >= 90:
        return "A"
    return "F"
```
`final_grade(95)` returns `"A"`; `final_grade(70)` returns `"F"`.

**8.**
```python
for name, info in student_data.items():
    average = sum(info["scores"]) / len(info["scores"])
    print(f"{name} ({info['course']}): {average:.1f}")
```
This prints `Ana (Data 101): 91.7`, `Ben (Data 101): 66.3`, and `Clara (Stats 210): 54.7`.

**9.**
```python
def build_report(name):
    info = student_data[name]
    summary = summaries[name]
    lines = [
        f"Student: {name}",
        f"Course:  {info['course']}",
        f"Average: {summary['average']:.1f}  Grade: {summary['grade']}",
        f"Attendance: {info['attendance'] * 100:.0f}%",
    ]
    if summary["grade"] == "A" and info["attendance"] >= 0.85:
        lines.append("Honor Roll")
    return "\n".join(lines)
```
Only Clara lacks the data — actually only **Ana** qualifies: she has grade `A` and attendance `0.90`. Ben has attendance `0.85` but grade `D`; Clara has grade `F`, so neither gets the line.

**10.** The project starts with variables holding a dictionary of student records, reads and formats text with f-strings, computes each average and letter grade using conditional logic, and routes everything through a single formatting function that the loop calls repeatedly — combining all the Basic-level skills into one working report generator.