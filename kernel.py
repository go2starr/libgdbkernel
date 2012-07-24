"""
kernel.py - A collection of gdb utilities for analyzing kernel core dumps
"""
import gdb
import re

from list_util import KIterator


#
# MACRO DEFINES - x86 specific for now!
#
PAGE_SHIFT = 12
PAGE_SIZE = 1 << PAGE_SHIFT

################################################################################
#
################################################################################
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



################################################################################
#
################################################################################
def dmesg(tail=10):
    __log_buf = gdb.parse_and_eval('__log_buf').address
    log_buf_len = gdb.parse_and_eval('log_buf_len')
    log_end = gdb.parse_and_eval('log_end') & (log_buf_len-1)
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


################################################################################
#
################################################################################

# Constants
SWP_USED = gdb.parse_and_eval('SWP_USED')
SWP_WRITEOK = gdb.parse_and_eval('SWP_WRITEOK')

# Globals
nr_swapfiles = gdb.parse_and_eval('nr_swapfiles')
nr_swap_pages = gdb.parse_and_eval('nr_swap_pages')
total_swap_pages = gdb.parse_and_eval('total_swap_pages')
total_swapcache_pages = gdb.parse_and_eval('swapper_space.nrpages')

def _global_page_state(key):
    return gdb.parse_and_eval('vm_stat[{0}].counter'.format(key))

def _totalram():
    return int(gdb.parse_and_eval('totalram_pages'))

def _sharedram():
    return 0

def _freeram():
    return _global_page_state('NR_FREE_PAGES')

def _bufferram():
    rv = 0
    for p in KIterator('all_bdevs', 'struct block_device', 'bd_list'):
        rv += int(p['bd_inode']['i_mapping']['nrpages'])
    return rv

def _cached():
    cached = _global_page_state('NR_FILE_PAGES')
    cached -= total_swapcache_pages
    cached -= _bufferram()
    return cached

def _totalhigh():
    return 0

def _freehigh():
    # UNIMPLEMENTED
    return -1

def _memunit():
    return PAGE_SIZE

def _swapinfo():
    nr_to_be_used = 0
    for type_ in range(nr_swapfiles):
        si = gdb.parse_and_eval("swap_info[{0}]".format(type_))
        if si['flags'] & SWP_USED and si['flags'] & SWP_WRITEOK:
            nr_to_be_used += si['inuse_pages']
    print nr_to_be_used
    freeswap = nr_swap_pages + nr_to_be_used
    totalswap = total_swap_pages + nr_to_be_used
    return {'freeswap' : int(freeswap),
            'totalswap' : int(totalswap)}

def K(x):
    return int(x << (PAGE_SHIFT - 10))

def mem_total():
    return K(_totalram())

def mem_free():
    return K(_freeram())

def mem_buff():
    return K(_bufferram())

def mem_cached():
    return K(_cached())

################################################################################
#
################################################################################
def ps_e():
    dic = {}
    for p in KIterator('init_task.tasks', 'struct task_struct', 'tasks'):
        pid = int(p['pid'])
        name = str(p['comm'])
        dic[pid] = name
    return dic


################################################################################
#
################################################################################
def __uname(name):
    return gdb.execute("""printf "%s", init_uts_ns.name.""" + name, True, True)
def unames():
    return __uname('sysname')
def unamen():
    return __uname('nodename')
def unamer():
    return __uname('release')
def unamev():
    return __uname('version')
def unamem():
    return __uname('machine')
def unamea():
    return '{0} {1} {2} {3} {4}'.format(unames(), unamen(), unamer(), unamev(), unamem())


################################################################################
#
################################################################################
