import json

from flask import Flask, Response

from app.db import Database, ReadWriteConnection, ReadOnlyConnection
from app.events import EventProcessor

_db = Database()
read_only_db = ReadOnlyConnection(_db)
event_processor = EventProcessor(ReadWriteConnection(_db), num_workers=1)
app = Flask("api")


@app.route("/students")
def students():
    with read_only_db as db:
        return json.dumps([student.to_json() for student in db.get_students().values()])


@app.route("/students/<student_id>")
def student_info(student_id):
    with read_only_db as db:
        student = db.get_students().get(student_id, None)
        if student:
            if student:
                return Response(json.dumps(student.to_json()), status=200)
        else:
            return Response(status=404)


@app.route("/exams")
def exams():
    with read_only_db as db:
        return json.dumps([exam.to_json() for exam in db.get_exams().values()])


@app.route("/exams/<exam_id>")
def exam_info(exam_id):
    with read_only_db as db:
        exam = db.get_exams().get(exam_id, None)
        if exam:
            return Response(json.dumps(exam.to_json()), status=200)
        else:
            return Response(status=404)


if __name__ == "__main__":
    event_processor.run()
    app.run(debug=True)
