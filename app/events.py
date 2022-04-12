import json
from threading import Thread

import requests


def event_stream(event_source, db):
    for line in event_source.events():
        if line.startswith(b"data:"):
            event = json.loads(line.split(b"data: ")[-1])
            student_id = event.get('studentId', None)
            exam_id = event.get('exam', None)
            score = event.get('score', None)
            if student_id and exam_id and score:
                with db as db_conn:
                    db_conn.new_student_exam(student_id, exam_id, score)


class EventProcessor:
    def __init__(self, event_source, database, num_workers=0):
        super().__init__()
        self.event_source = event_source
        self.database = database
        self.num_workers = num_workers
        self.workers = []

    def run(self):
        for _ in range(self.num_workers):
            worker = Thread(target=event_stream, args=(self.event_source, self.database,))
            self.workers.append(worker)
            worker.start()

    def shutdown(self):
        for worker in self.workers:
            worker.join()


class EventSource:
    def events(self):
        response = requests.get("https://live-test-scores.herokuapp.com/scores", stream=True)
        return response.iter_lines()
