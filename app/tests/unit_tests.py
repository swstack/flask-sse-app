import unittest
import threading

from app.db import Database, ReadWriteConnection


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

    def test_db_paging(self):
        self.db.new_student_exam("a", "exam1", 100)
        self.db.new_student_exam("z", "exam1", 100)
        self.db.new_student_exam("b", "exam1", 100)
        self.db.new_student_exam("d", "exam1", 100)
        self.db.new_student_exam("k", "exam1", 100)
        self.db.new_student_exam("t", "exam1", 100)
        self.db.new_student_exam("f", "exam1", 100)

        page1, next_page = self.db.get_student_page(1, 2)
        assert len(page1) == 2
        assert next_page == True
        assert page1[0].student_id == "a"
        assert page1[1].student_id == "b"

        page2, next_page = self.db.get_student_page(2, 2)
        assert len(page2) == 2
        assert next_page == True
        assert page2[0].student_id == "d"
        assert page2[1].student_id == "f"

        page3, next_page = self.db.get_student_page(3, 2)
        assert len(page3) == 2
        assert next_page == True
        assert page3[0].student_id == "k"
        assert page3[1].student_id == "t"

        page4, next_page = self.db.get_student_page(4, 2)
        assert len(page4) == 1
        assert next_page == False
        assert page4[0].student_id == "z"

        page5, next_page = self.db.get_student_page(5, 2)
        assert len(page5) == 0
        assert next_page == False

    def test_read_write_connection(self):
        read_write_conn1 = ReadWriteConnection(self.db, wait=False)
        read_write_conn2 = ReadWriteConnection(self.db, wait=False)

        def thread():
            try:
                with read_write_conn2:
                    pass
            except Exception as e:
                assert f"{e}" == "Failed to acquire lock"

        with read_write_conn1:
            t = threading.Thread(target=thread)
            t.start()
            t.join()


if __name__ == "__main__":
    unittest.main()
