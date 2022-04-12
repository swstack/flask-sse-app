import unittest

from app.api import create_app
from app.db import Database, ReadWriteConnection
from app.events import EventProcessor
from app.tests.mocks import MockEventSource


class TestAPI(unittest.TestCase):
    """These are integration tests that mock as little as possible and for the most part
    treat the entire application/api as a black box"""

    def setUp(self) -> None:
        self.db = Database()
        self.event_source = MockEventSource()
        self.event_processor = EventProcessor(self.event_source, ReadWriteConnection(self.db),
                                              num_workers=1)
        self.app = create_app(self.db)
        self.event_processor.run()

    def tearDown(self) -> None:
        self.event_source.shutdown()
        self.event_processor.shutdown()

    def test_students(self):
        client = self.app.test_client()
        response = client.get("/students")
        assert response.status_code == 200
        students = response.json
        assert len(students) == 0

        # Add first student with first exam with score of 100
        self.event_source.new_event({"studentId": "student1", "exam": 1, "score": 100})

        students = client.get("/students").json
        assert len(students) == 1
        student = client.get(f"/students/student1").json
        assert student["id"] == "student1"
        assert student["average"] == 100
        assert len(student["exams"]) == 1

        # Add same student with second exam with score of 80
        self.event_source.new_event({"studentId": "student1", "exam": 2, "score": 80})

        students = client.get("/students").json
        assert len(students) == 1
        student = client.get(f"/students/student1").json
        assert student["average"] == 90
        assert len(student["exams"]) == 2

        # Add a new student for exam 2 with score 60
        self.event_source.new_event({"studentId": "student2", "exam": 2, "score": 60})

        students = client.get("/students").json
        assert len(students) == 2
        student1 = client.get(f"/students/student1").json
        student2 = client.get(f"/students/student2").json
        assert student2["id"] == "student2"
        assert student2["average"] == 60
        assert student1["average"] == 90
        assert len(student1["exams"]) == 2

    def test_exams(self):
        client = self.app.test_client()
        response = client.get("/exams")
        assert response.status_code == 200
        exams = response.json
        assert len(exams) == 0

        # Add first student with first exam with score of 100
        self.event_source.new_event({"studentId": "student1", "exam": 1, "score": 100})

        exams = client.get("/exams").json
        assert len(exams) == 1
        exam = client.get("/exams/1").json
        assert exam["id"] == 1
        assert exam["average"] == 100
        assert len(exam["students"]) == 1

        # Add same student with second exam with score of 80
        self.event_source.new_event({"studentId": "student1", "exam": 2, "score": 80})

        exams = client.get("/exams").json
        assert len(exams) == 2
        exam = client.get("/exams/2").json
        assert exam["id"] == 2
        assert exam["average"] == 80
        assert len(exam["students"]) == 1

        # Add a new student for exam 2 with score 60
        self.event_source.new_event({"studentId": "student2", "exam": 2, "score": 60})

        exams = client.get("/exams").json
        assert len(exams) == 2
        exam = client.get("/exams/2").json
        assert exam["average"] == 70
        assert len(exam["students"]) == 2


if __name__ == "__main__":
    unittest.main()
