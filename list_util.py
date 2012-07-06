"""
list_util.py - list manipulation utilities for debugging the kernel
"""

def _offsetof(type_, member):
    s = '(size_t) &((%(type)s *)0)->%(member)s' % \
        {'type':type_, 'member':member}
    return gdb.parse_and_eval(s)

def _container_of(ptr, type_, member):
    s = '*(%(type)s *)((char *)%(ptr)s - %(off)d)' % \
        {'ptr':ptr, 'type':type_, 'off':_offsetof(type_, member)}
    return gdb.parse_and_eval(s)

def _list_entry(list_, type_, member):
    return _container_of(list_, type_, member)

def _list_head(list_, type_, member):
    next_ = gdb.parse_and_eval(list_ + '->next')
    return _list_entry(next_, type_, member)

def _list_tail(list_, type_, member):
    prev = gdb.parse_and_eval(list_ + '->prev')
    return _list_entry(prev, type_, member)

class KIterator(object):
    """An object to iterate over elements of a kernel list.
    Constructed with list_head identifier, containing struct type, and
    containing identifier.
    """
    def __init__(self, list_, type_, member):
        self.list_ = gdb.parse_and_eval(list_)
        self.type_ = type_
        self.member = member
        self.pos = gdb.parse_and_eval(list_)
        
    def next(self):
        self.pos = gdb.parse_and_eval('*((struct list_head *)' + 
                                      str(self.pos['next']) + ')')

        if self.pos.address == self.list_.address:
            raise StopIteration

        return _list_entry(self.pos.address, self.type_, self.member)

    def __iter__(self):
        return self    

