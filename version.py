"""
version.py - Functions relating to the kernel version/crashing system
"""
import gdb

from kernel import *

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
    return '{} {} {} {} {}'.format(unames(), unamen(), unamer(), unamenv(), unamem())
    
