import json
from threading import Thread

import requests


def event_stream(db):
    response = requests.get("https://live-test-scores.herokuapp.com/scores", stream=True)
    for line in response.iter_lines():
        if line.startswith(b"data:"):
            event = json.loads(line.split(b"data: ")[-1])
            student_id = event.get('studentId', None)
            exam_id = event.get('exam', None)
            score = event.get('score', None)
            if student_id and exam_id and score:
                with db as db_conn:
                    db_conn.new_student_exam(student_id, exam_id, score)


class EventProcessor:
    def __init__(self, database, num_workers=0):
        super().__init__()
        self.database = database
        self.num_workers = num_workers
        self.workers = []

    def run(self):
        for _ in range(self.num_workers):
            worker = Thread(target=event_stream, args=(self.database,))
            self.workers.append(worker)
            worker.start()
