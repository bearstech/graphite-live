from tornado.web import RequestHandler, asynchronous, Application
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop, PeriodicCallback
# Inspiration from
# https://github.com/guyzmo/event-source-library/blob/master/eventsource/listener.py


class Emitter(object):

    def __init__(self):
        self.chans = {}

    def add(self, chan, cb):
        if chan not in self.chans:
            self.chans[chan] = []
        self.chans[chan].append(cb)

    def remove(self, chan, cb):
        if chan in self.chans:
            self.chans[chan].remove(cb)

    def emit(self, chan, *args, **dargs):
        if chan in self.chans:
            for cb in self.chans[chan]:
                cb(*args, **dargs)


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
            self.events.emit('*', len(response.body))

    def watch_for(self, url):
        self.targets.add(url)


class EventSourceHandler(RequestHandler):

    def initialize(self, events, clients):
        self.events = events
        self.clients = clients
        self.request.connection.set_close_callback(self.on_closing)

    def on_closing(self):
        self.events.remove('*', self.on_event)

    def on_event(self, evt):
        self.write("data: %s\n\n" % evt)
        self.flush()

    @asynchronous
    def get(self):

        def closing():
            print "Il va falloir rentrer, monsieur"

        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")

        self.events.add('*', self.on_event)

    def on_finish(self):
        print "Finishing", self

if __name__ == "__main__":
    import sys
    events = Emitter()
    application = Application([
        (r"/", EventSourceHandler, dict(events=events, clients=[])),
    ])
    application.listen(8888)
    client = GraphiteClient(events=events)
    client.watch_for(sys.argv[1])
    IOLoop.instance().start()
