"""
proc.py - Functions relating to processes 
"""
import gdb

from list_util import KIterator
from kernel import *

def ps_e():
    dic = {}
    for p in KIterator('init_task.tasks', 'struct task_struct', 'tasks'):
        pid = int(p['pid'])
        name = str(p['comm'])
        dic[pid] = name
    return dic
