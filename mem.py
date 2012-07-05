"""
mem.py - Functions relating to kernel memory
"""
import gdb

from kernel import *
from list_util import KIterator

# Constants
SWP_USED = gdb.parse_and_eval('SWP_USED')
SWP_WRITEOK = gdb.parse_and_eval('SWP_WRITEOK')

# Globals
nr_swapfiles = gdb.parse_and_eval('nr_swapfiles')
nr_swap_pages = gdb.parse_and_eval('nr_swap_pages')
total_swap_pages = gdb.parse_and_eval('total_swap_pages')
total_swapcache_pages = gdb.parse_and_eval('swapper_space.nrpages')

def _global_page_state(key):
    return gdb.parse_and_eval('vm_stat[{}].counter'.format(key))

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
        si = gdb.parse_and_eval("swap_info[{}]".format(type_))
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
