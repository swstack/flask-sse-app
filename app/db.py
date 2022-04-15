"""
There is a many-to-many relationship between students and exams

If this were SQL I would use a fully normalized data model with proper indexing to
achieve fast lookups based on exam_id's and student_id's.

Student:
    id (primary key)

Exam:
    id (primary key)

StudentExam:
    id (primary key)
    student_id (fk)
    exam_id (fk)
    score

In memory I will store it a little differently to optimize access patterns.
"""

import json
from threading import RLock


class Serializable:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        return json.loads(self.to_json())


class Student(Serializable):
    def __init__(self, student_id):
        self.student_id = student_id
        self.student_exams = {}
        self.student_average = -1

    def recompute_average(self):
        student_exam_scores = [exam.score for exam in self.student_exams.values()]
        self.student_average = sum(student_exam_scores) / len(student_exam_scores)


class Exam(Serializable):
    def __init__(self, exam_id):
        self.exam_id = exam_id
        self.all_student_exams = {}
        self.all_student_average = -1

    def recompute_average(self):
        exam_scores = [exam.score for exam in self.all_student_exams.values()]
        self.all_student_average = sum(exam_scores) / len(exam_scores)


class StudentExam(Serializable):
    def __init__(self, student_id, exam_id, score):
        self.student_id = student_id
        self.exam_id = exam_id
        self.score = score


class Database:
    def __init__(self):
        self.students_index = {}
        self.exams_index = {}
        self.lock = RLock()

    def new_student_exam(self, student_id, exam_id, score):
        student_exam = StudentExam(student_id, exam_id, score)

        student = self.students_index.get(student_id, Student(student_id))
        student.student_exams[exam_id] = student_exam
        student.recompute_average()
        self.students_index[student_id] = student

        exam = self.exams_index.get(exam_id, Exam(exam_id))
        exam.all_student_exams[student_id] = student_exam
        exam.recompute_average()
        self.exams_index[exam_id] = exam

    def get_student_page(self, page, size):
        students_sorted = sorted(self.students_index)
        start = (page - 1) * size
        end = min(start + size, len(students_sorted))
        next_page = end < len(students_sorted)
        page_data = students_sorted[start:end]
        return [self.students_index.get(k) for k in page_data], next_page

    def get_students(self):
        return self.students_index

    def get_exams(self):
        return self.exams_index


class ReadWriteConnection:
    def __init__(self, db, wait=True):
        self.db = db
        self.wait = wait

    def __enter__(self):
        if self.db.lock.acquire(blocking=self.wait):
            return self.db
        else:
            raise RuntimeError("Failed to acquire lock")

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.db.lock.release()


class ReadOnlyConnection:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass
