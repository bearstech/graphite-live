
class Iterator(object):

    def __init__(self, start, step, values):
        self.start = start
        self.step = step
        self.values = values

    def __iter__(self):
        for value in self.values:
            if value != "None":
                yield self.start, float(value)
            self.start += self.step


def raw2list(raw):
    keys, values = raw.split('|')
    keys = keys.split(',')
    start, end, step = keys[-3:]
    name = keys[:-3]
    values = values.split(',')
    start = int(start)
    step = int(step)
    return ",".join(name), Iterator(start, step, values)


if __name__ == "__main__":
    raw = """sumSeries(servers.petzamp.cpu.cpu0.idle,servers.petzamp.cpu.cpu1.idle),1365418770,1365420570,15|None,None,None,None,None,None,355.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,347.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,368.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,356.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,352.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,363.0,None,None,None,None,None,None,None,None,None,None,None,None,None"""
    name, values = raw2list(raw)
    print name
    print list(values)
