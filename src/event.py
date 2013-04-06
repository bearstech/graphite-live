
class Emitter(object):
    """
    Event emitter just like in javascript.
    You have to remove every added callback or your application will leak.
    """

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
