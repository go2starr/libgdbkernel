"""
bt.py - Functions relating to the backtrace and stack 
"""
import re

def backtrace(count=0):
    bt = []
    bt_tmpl = re.compile('#\d+  (?P<entry>.*)')
    if count == 0:
        count = ""

    backtrace = gdb.execute("bt {0}".format(str(count)), True, True).strip().split('\n')

    for line in backtrace:
        m = bt_tmpl.search(line)
        if m:
            bt.append(m.group('entry'))
    return bt

def backtrace_top():
    return backtrace(1)

