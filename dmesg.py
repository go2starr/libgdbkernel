"""
log.py - Functions relating to kernel log buffers
"""
import gdb

def dmesg():
    __log_buf = gdb.parse_and_eval('__log_buf').address
    log_end = gdb.parse_and_eval('log_end')
    dmesg = ""
    for i in range(log_end):
        dmesg += gdb.execute('printf "%c", ((char *)({}))[{}]'.format(__log_buf, i), True, True)[0]
    return dmesg


