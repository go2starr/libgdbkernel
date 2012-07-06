"""
log.py - Functions relating to kernel log buffers
"""

def dmesg(tail=10):
    __log_buf = gdb.parse_and_eval('__log_buf').address
    log_end = gdb.parse_and_eval('log_end')
    dmesg = []
    line = []
    for i in range(log_end):
        if not tail:
            break
        c = gdb.execute('printf "%c", ((char *)({0}))[{1}]'.format(
                __log_buf, log_end - 1 - i), True, True)[0]
        line.insert(0, c)
        if c == '\n':
            dmesg.insert(0, "".join(line))
            line = []
            tail -= 1
    return "".join(dmesg)


