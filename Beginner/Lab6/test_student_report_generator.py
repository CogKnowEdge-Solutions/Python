"""Tests for Lab 6 — Student Report Generator (Mini Project).

Covers:
- final_grade() function — all branches
- build_report() function — output correctness
- Honor roll logic (exercise addition)
- Edge cases and consistency
"""
import pytest


def final_grade(exam_score, assignments_completed):
    """Re-implementation of Lab 6 final_grade for testing."""
    if exam_score >= 90 and assignments_completed:
        return "A"
    elif exam_score >= 80 and assignments_completed:
        return "B"
    elif exam_score >= 70 and assignments_completed:
        return "C"
    elif exam_score >= 60 and assignments_completed:
        return "D"
    else:
        return "F"


def build_report(students):
    """Re-implementation of Lab 6 build_report for testing."""
    report = {}
    for name, data in students.items():
        exam = data["exam"]
        hw = data["assignments_completed"]
        grade = final_grade(exam, hw)
        avg = exam
        report[name] = {"grade": grade, "average": avg}
    return report


class TestFinalGradeBranches:
    """Test every branch of final_grade for Lab 6."""

    def test_grade_a(self):
        assert final_grade(95, True) == "A"

    def test_grade_a_boundary(self):
        assert final_grade(90, True) == "A"

    def test_grade_b(self):
        assert final_grade(85, True) == "B"

    def test_grade_b_boundary(self):
        assert final_grade(80, True) == "B"

    def test_grade_c(self):
        assert final_grade(75, True) == "C"

    def test_grade_c_boundary(self):
        assert final_grade(70, True) == "C"

    def test_grade_d(self):
        assert final_grade(65, True) == "D"

    def test_grade_d_boundary(self):
        assert final_grade(60, True) == "D"

    def test_grade_f_low_score(self):
        assert final_grade(50, True) == "F"

    def test_grade_f_no_assignments(self):
        assert final_grade(95, False) == "F"

    def test_grade_f_zero(self):
        assert final_grade(0, False) == "F"

    def test_all_branches_covered(self):
        """Verify all five grade branches are reachable."""
        branches = set()
        branches.add(final_grade(95, True))  # A
        branches.add(final_grade(85, True))  # B
        branches.add(final_grade(75, True))  # C
        branches.add(final_grade(65, True))  # D
        branches.add(final_grade(30, True))  # F
        assert branches == {"A", "B", "C", "D", "F"}


class TestBuildReport:
    """Test build_report function output."""

    def test_report_structure(self):
        students = {
            "Ana": {"exam": 95, "assignments_completed": True},
        }
        report = build_report(students)
        assert "Ana" in report
        assert "grade" in report["Ana"]
        assert "average" in report["Ana"]

    def test_report_ana(self):
        students = {
            "Ana": {"exam": 95, "assignments_completed": True},
        }
        report = build_report(students)
        assert report["Ana"]["grade"] == "A"
        assert report["Ana"]["average"] == 95

    def test_report_ben(self):
        students = {
            "Ben": {"exam": 66, "assignments_completed": True},
        }
        report = build_report(students)
        assert report["Ben"]["grade"] == "D"

    def test_report_clara(self):
        students = {
            "Clara": {"exam": 50, "assignments_completed": True},
        }
        report = build_report(students)
        assert report["Clara"]["grade"] == "F"

    def test_multiple_students(self):
        students = {
            "Ana": {"exam": 95, "assignments_completed": True},
            "Ben": {"exam": 66, "assignments_completed": True},
            "Clara": {"exam": 50, "assignments_completed": True},
        }
        report = build_report(students)
        assert len(report) == 3
        assert report["Ana"]["grade"] == "A"
        assert report["Ben"]["grade"] == "D"
        assert report["Clara"]["grade"] == "F"

    def test_report_deterministic(self):
        students = {"Ana": {"exam": 85, "assignments_completed": True}}
        r1 = build_report(students)
        r2 = build_report(students)
        assert r1 == r2


class TestHonorRoll:
    """Test honor roll exercise logic."""

    def check_honor_roll(self, grade, attendance_rate):
        return grade == "A" and attendance_rate >= 0.85

    def test_ana_qualifies(self):
        assert self.check_honor_roll("A", 0.95) is True

    def test_ben_fails_grade(self):
        assert self.check_honor_roll("D", 0.90) is False

    def test_clara_fails_attendance(self):
        assert self.check_honor_roll("A", 0.78) is False

    def test_dan_fails_both(self):
        assert self.check_honor_roll("C", 0.70) is False

    def test_boundary_attendance_exact(self):
        assert self.check_honor_roll("A", 0.85) is True

    def test_boundary_attendance_just_below(self):
        assert self.check_honor_roll("A", 0.84) is False

    def test_only_ana_qualifies(self):
        """Verify only Ana qualifies with given data."""
        students = {
            "Ana": {"grade": "A", "attendance": 0.95},
            "Ben": {"grade": "D", "attendance": 0.90},
            "Clara": {"grade": "A", "attendance": 0.78},
            "Dan": {"grade": "C", "attendance": 0.70},
        }
        honor = [
            name for name, data in students.items()
            if self.check_honor_roll(data["grade"], data["attendance"])
        ]
        assert honor == ["Ana"]
