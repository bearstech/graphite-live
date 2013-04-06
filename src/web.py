from tornado.web import RequestHandler, asynchronous, Application
from tornado.httpserver import HTTPServer
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop, PeriodicCallback

from event import Emitter


class GraphiteClient(object):

    def __init__(self, events, tempo=10):
        self.events = events
        self.targets = set()
        self.client = HTTPClient()
        self.loop = PeriodicCallback(self._fetch, tempo * 1000)
        self.loop.start()

    def _fetch(self):
        for url in self.targets:
            response = self.client.fetch(url)
            self.events.emit('*', response.body)

    def watch_for(self, url):
        self.targets.add(url)


class EventSourceHandler(RequestHandler):

    def initialize(self, events, clients):
        self.events = events
        self.clients = clients

    def _on_closing(self):
        self.events.remove('*', self._on_event)

    def _on_event(self, evt):
        self.write("data: %s\n\n" % evt)
        self.flush()

    @asynchronous
    def get(self):
        self.set_status(200)
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")

        self.events.add('*', self._on_event)
        self.request.connection.set_close_callback(self._on_closing)


if __name__ == "__main__":
    import sys
    events = Emitter()
    application = Application([
        (r"/", EventSourceHandler, dict(events=events, clients=[])),
    ], debug=True)
    server = HTTPServer(application, no_keep_alive=True, xheaders=True)
    server.listen(8888)
    client = GraphiteClient(events=events)
    client.watch_for(sys.argv[1])
    IOLoop.instance().start()
