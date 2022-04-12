import json
import queue
import time


class MockEventSource:
    def __init__(self):
        self.event_stream = queue.Queue()
        self.shutdown_flag = False

    def events(self):
        while not self.shutdown_flag:
            try:
                event = self.event_stream.get(block=False, timeout=0.1)
                yield event
            except queue.Empty:
                continue

    def new_event(self, event):
        self.event_stream.put(str.encode(f"data: {json.dumps(event)}"))
        # Since the ingestion of events is async we must guarantee that the event has been
        # processed, we could make a more elaborate mechanism for this but for the sake of this
        # toy project let's just do a small sleep (not ideal I know)
        time.sleep(0.5)

    def shutdown(self):
        self.shutdown_flag = True
