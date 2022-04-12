import json

from flask import Flask, Response

from app.db import ReadOnlyConnection


def create_app(database):
    read_only_db = ReadOnlyConnection(database)
    app = Flask("api")

    @app.route("/students")
    def students():
        # TODO: Support pagination
        with read_only_db as db:
            return respond(
                json.dumps([student_json(student) for student in db.get_students().values()]))

    @app.route("/students/<student_id>")
    def student_info(student_id):
        with read_only_db as db:
            student = db.get_students().get(student_id, None)
            if student:
                if student:
                    return respond(json.dumps(student_json(student)))
            else:
                return respond(status=404)

    @app.route("/exams")
    def exams():
        # TODO: Support pagination
        with read_only_db as db:
            return respond(json.dumps([exam_json(exam) for exam in db.get_exams().values()]))

    @app.route("/exams/<int:exam_id>")
    def exam_info(exam_id):
        with read_only_db as db:
            exam = db.get_exams().get(exam_id, None)
            if exam:
                return respond(json.dumps(exam_json(exam)))
            else:
                return respond(status=404)

    return app


def student_json(student):
    return {
        "id": student.student_id,
        "average": student.student_average,
        "exams": list(student.student_exams.keys())
    }


def exam_json(exam):
    return {
        "id": exam.exam_id,
        "average": exam.all_student_average,
        "students": list(exam.all_student_exams.keys())
    }


def respond(body=None, status=200, content_type="application/json"):
    return Response(body, status=status, content_type=content_type)
