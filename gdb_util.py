#
# gdb_util.py - A collection of py/gdb utilities
#

import re

# Filter function pointers with complex return value or arguments by paren
RE_NOT_PAREN = '[^()]'
RE_ENUM = '^(const )?(enum){}+'.format(RE_NOT_PAREN)
RE_STRUCT = '^(const )?(struct){}+'.format(RE_NOT_PAREN)
RE_UNION = '^(const )?(union){}+'.format(RE_NOT_PAREN)
RE_ARRAY= '^(const )?({}*\[\d+\]{}*)'.format(RE_NOT_PAREN, RE_NOT_PAREN)

def is_complex_type(type_):
    """Returns true if the type is an enum, union, or array """
    return re.search('{}|{}|{}'.format(RE_STRUCT, RE_UNION, RE_ARRAY),
                                       type_) and not is_pointer_type(type_)
def is_pointer_type(type_):
    """Returns true if the type is a pointer"""
    return '*' in type_

def is_union_type(type_):
    """Returns true if the type is a union"""
    return re.search(RE_UNION, type_)

def is_enum_type(type_):
    """Returns true if the type is an enum"""
    return re.search(RE_ENUM, type_)

def is_array_type(type_):
    """Returns true if the type is an array"""
    return re.search(RE_ARRAY, type_)

def is_struct_type(type_):
    """Returns true if the type is a struct"""
    return re.search(RE_STRUCT, type_)

def get_array_length(type_):
    """ Returns the array length given the type.  0 if not an array """
    m = re.search('\[(\d+)\]', type_)
    if m: 
        return int(m.group(1))
    else:
        return 0

def to_dict(g_val):
    """Used to convert gdbValues into python dictionaries"""
    dic = {}
    type_ = str(g_val.type)

    # End recursion on base types
    if not is_complex_type(type_):
        return g_val.__str__()
    # Arrays
    elif is_array_type(type_):
        l = get_array_length(type_)
        for i in range(l):
            dic[i] = to_dict(g_val[i])
    # Enum
    elif is_enum_type(type_):
        raise ValueError("Unsupported type: " + str(g_val.type))
    # Union/Struct
    elif is_union_type(type_) or is_struct_type(type_):
        fields = g_val.type.fields()
        for f in fields:
            f_name = str(f.name)
            f_val = g_val[f_name]
            dic[f_name] = to_dict(f_val)
    else:
        raise ValueError("Unsupported type: " + str(g_val.type))
    return dic

def identifier_to_dict(identifier):
    """Given an identifier, returns a dictionary of the identifier's fields"""
    struct = gdb.parse_and_eval(identifier)
    return to_dict(struct)
    
