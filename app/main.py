from app.api import create_app
from app.db import Database, ReadWriteConnection
from app.events import EventProcessor, EventSource

if __name__ == "__main__":
    db = Database()
    event_source = EventSource()
    event_processor = EventProcessor(event_source, ReadWriteConnection(db), num_workers=5)
    app = create_app(db)
    event_processor.run()
    app.run(debug=True)
