def raw2list(raw):
    keys, values = raw.split('|')
    start, end, step = keys.split(',')[-3:]
    values = values.split(',')
    start = int(start)
    step = int(step)
    for value in values:
        if value != "None":
            yield start, float(value)
        start += step


if __name__ == "__main__":
    raw = """sumSeries(servers.petzamp.cpu.cpu0.idle,servers.petzamp.cpu.cpu1.idle),1365418770,1365420570,15|None,None,None,None,None,None,355.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,347.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,368.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,356.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,352.0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,363.0,None,None,None,None,None,None,None,None,None,None,None,None,None"""
    print list(raw2list(raw))
