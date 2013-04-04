from tornado.web import RequestHandler, asynchronous, Application
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop, PeriodicCallback
# Inspiration from
# https://github.com/guyzmo/event-source-library/blob/master/eventsource/listener.py


class GraphiteClient(object):

    def __init__(self, tempo=10):
        self.targets = set()
        self.client = HTTPClient()
        self.loop = PeriodicCallback(self._fetch, tempo * 1000)
        self.loop.start()

    def _fetch(self):
        print "toto"
        for url in self.targets:
            response = self.client.fetch(url)
            print response.body


    def watch_for(self, url):
        self.targets.add(url)


class EventSourceHandler(RequestHandler):

    def initialize(self, clients):
        self.clients = clients

    @asynchronous
    def get(self, action, target):
        self.set_header("Content-Type", "text/event-stream")
        self.set_header("Cache-Control", "no-cache")
        self.flush()

    def on_finish(self):
        pass

if __name__ == "__main__":
    application = Application([
        (r"/", EventSourceHandler, dict(clients=[])),
    ])
    application.listen(8888)
    client = GraphiteClient()
    IOLoop.instance().start()
