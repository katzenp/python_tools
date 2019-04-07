"""
utils.py

Description:
    Tools and utilitites that manage, support, and extend native Python objects
"""
SEPARATOR = "{name:{fill}{align}{width}}"
DEFAULT_SEPARATOR = SEPARATOR.format(name="", fill="-", align="<", width=80)


# =============================================================================
# object attribute inspection
# =============================================================================
def accumulate_object_attrs(obj, accumulator):
    """
    Collects object attribute inheritance information for the given object

    :param obj: the object to inspect
    :type obj: any 
    :param accumulator: data structure used to store the information
    :type accumulator: list
    :return: n/a
    :rtype: n/a
    """
    attrs = []
    if hasattr(obj, "__dict__"):
        attrs = sorted(obj.__dict__.keys())
    else:
        attrs = dir(obj)
    obj_data = (obj, attrs)
    accumulator.append(obj_data)

    bases = getattr(obj, "__bases__", [])
    for b in bases:
        accumulate_object_attrs(b, accumulator)


def print_object_attrs(obj):
    """
    Displays where each of the given object's attributes is inherited from

    :param obj: the object to inspect
    :type obj: any
    :return: n/a
    :rtype: n/a
    """
    print(DEFAULT_SEPARATOR)
    print(type(obj))
    print(DEFAULT_SEPARATOR)
    if hasattr(obj, "__dict__"):
        for a in obj.__dict__.keys():
            print(a)
    else:
        for a in dir(obj):
            print(a)

    bases = getattr(obj, "__bases__", [])
    for b in bases:
        print_object_attrs(b)


# ==============================================================================
# call display
# ==============================================================================
def repr_call(func, *func_args, **func_kwargs):
    """
    Returns a string representation of a call to the given function

    :param func: function object
    :type func: any callable object
    :param *func_args: the function object's positional paramters
    :type *func_args: tuple
    :param **func_kwargs: the function object's keyword paramters
    :type **func_kwargs: dict
    :return: timed function object
    :rtype: function object
    """
    # get signature
    signature = "{}(".format(func.__name__)
    for each in func_args:
        signature += "{!r}, ".format(each)
    for k, v in func_kwargs.iteritems():
        signature += "{}={!r}, ".format(k, v)
    signature = signature[:-2]
    signature += ")"

    return signature


def format_calls(calls_strings):
    """
    Returns a formatted display of all given call strings like:
        ---------------------------------------
        func_name(arg, arg, kw=value, kw=value)
        ...
        ---------------------------------------

    :param calls_strings: list of call strings
    :type calls_strings: list
    :return: a formatted display of all call strings
    :rtype: string
    """
    # get longest command str
    width = 0
    for each in calls_strings:
        count = len(each)
        if count > width:
            width = count

    # print commands that got run
    calls = "\n".join(calls_strings)
    report = "{sep:{fill}<{width}s}\n{calls}\n{sep:{fill}<{width}s}".format(
        sep="",
        fill="-",
        width=width,
        calls=calls)
    return report


# ==============================================================================
# hierarchiews
# ==============================================================================
def walker(root, accumulator, func, *func_args, **func_kwargs):
    """
    Recursive hierarchy walker. Walking begins at the given root node and
    traverses its hierarchy based on the behavior of the specified traversal function
    Results are collected into an accumulator object and always include the root node

    :param root: hierarchy root node
    :type root: any
    :param accumulator: data structure to for storing results
    :type accumulator: list
    :param func: cthe allable object used to traverse a hierarchy
    :type func: any callable object
    :param *func_args: miscellaneous positional parameters to the traversal function
    :type *func_args: tuple
    :param **func_kwargs: miscellaneous keyword parameters to the traversal function
    :type **func_kwargs: dict
    :return: n/a
    :rtype: n/a
    """
    # collect results
    accumulator.append(root)

    # get descendants/ancestors
    try:
        result = func(root, *func_args, **func_kwargs) or []
    except Exception:
        result = []

    # walk !
    for each in result:
        walk(accumulator, func, each, *func_args, **func_kwargs)


print_object_attrs([])
