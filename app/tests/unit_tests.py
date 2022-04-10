import unittest

from app.db import Database


class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database()

    def test_add_student_exam(self):
        # Add first student with first exam with score of 100
        self.db.new_student_exam("student1", "exam1", 100)

        students = self.db.get_students()
        assert len(students) == 1
        assert students.get("student1").student_id == "student1"
        assert students.get("student1").student_average == 100
        assert students.get("student1").student_exams.get("exam1").exam_id == "exam1"
        assert students.get("student1").student_exams.get("exam1").score == 100
        assert len(students.get("student1").student_exams) == 1

        exams = self.db.get_exams()
        assert len(exams) == 1
        assert exams.get("exam1").exam_id == "exam1"
        assert exams.get("exam1").all_student_average == 100
        assert exams.get("exam1").all_student_exams.get("student1").student_id == "student1"
        assert len(exams.get("exam1").all_student_exams) == 1

        # Add same student with second exam with score of 80
        self.db.new_student_exam("student1", "exam2", 80)

        students = self.db.get_students()
        assert len(students) == 1
        assert students.get("student1").student_average == 90
        assert students.get("student1").student_exams.get("exam2").exam_id == "exam2"
        assert students.get("student1").student_exams.get("exam2").score == 80
        assert len(students.get("student1").student_exams) == 2

        exams = self.db.get_exams()
        assert len(exams) == 2
        assert exams.get("exam2").exam_id == "exam2"
        assert exams.get("exam2").all_student_average == 80
        assert exams.get("exam2").all_student_exams.get("student1").student_id == "student1"
        assert len(exams.get("exam2").all_student_exams) == 1

        # Add a new student for exam 2 with score 60
        self.db.new_student_exam("student2", "exam2", 60)

        students = self.db.get_students()
        assert len(students) == 2
        assert students.get("student2").student_id == "student2"
        assert students.get("student2").student_average == 60
        assert students.get("student1").student_average == 90
        assert students.get("student2").student_exams.get("exam2").exam_id == "exam2"
        assert students.get("student2").student_exams.get("exam2").score == 60
        assert len(students.get("student1").student_exams) == 2

        exams = self.db.get_exams()
        assert len(exams) == 2
        assert exams.get("exam2").all_student_average == 70
        assert exams.get("exam2").all_student_exams.get("student2").student_id == "student2"
        assert len(exams.get("exam2").all_student_exams) == 2

    def test_read_write_connection(self):
        pass


if __name__ == "__main__":
    unittest.main()
