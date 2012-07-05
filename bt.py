"""
bt.py - Functions relating to the backtrace and stack 
"""
import gdb
import re

def backtrace():
    bt = []
    bt_tmpl = re.compile('#\d+  (?P<entry>.*)')

    backtrace = gdb.execute('bt', True, True).strip().split('\n')

    for line in backtrace:
        m = bt_tmpl.search(line)
        if m:
            bt.append(m.group('entry'))
    return bt

def backtrace_top():
    return backtrace()[0]

