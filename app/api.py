import json
from flask import Flask, Response, request

from app.db import ReadOnlyConnection


def create_app(database):
    read_only_db = ReadOnlyConnection(database)
    app = Flask("api")

    @app.route("/students")
    def students():
        page = request.args.get("page", None)
        size = request.args.get("size", None)

        with read_only_db as db:

            if page and size:
                current_page, is_next_page = db.get_student_page(int(page), int(size))
                next_page = None
                if is_next_page:
                    next_page = int(page) + 1
                return student_page(current_page, page, next_page)
            else:
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


def student_page(students, page, next_page):
    return {
        "students": [student_json(student) for student in students],
        "page": page,
        "nextPage": next_page,
    }


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
