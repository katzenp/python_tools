"""
bases.py

Description:
    Generic Python base classes
"""

# ==============================================================================
# object introspection
# ==============================================================================
class ClassPrinter(object):
    """
    Class for printing/displaying object inheritance information
    """
    DIVIDER = '\n{chr:{fill}{align}{width}}\n'.format(
        chr="", fill="-", align="<", width=60
    )

    def print_tree(self):
        """
        
        Prints out the inheritance tree including all attributes

        :return: n/a
        :rtype: n/a
        """
        # Instance attributes
        print('\n')
        print(self.DIVIDER)
        print("Instance:  of <class '{}'>".format(self.__class__.__name__))
        for key, value in sorted(self.__dict__.items()):
            print("\t{} : {}".format(key, type(value)))

        # Class attributes
        print(self.DIVIDER)
        print("Class : {}".format(self.__class__.__name__))
        for key, value in sorted(self.__class__.__dict__.items()):
            print("\t{} : {}".format(key, type(value)))

        # Base class attributes
        print(self.DIVIDER)
        for base in self.__class__.__bases__:
            print("Base Class : {}".format(base.__name__))
            for key, value in sorted(base.__dict__.items()):
                print("\t{} : {}".format(key, type(value)))

    # --------------------------------------------------------------------------
    # operator overloads
    # --------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of this object

        :return: string representation of this object
        :rtype: string
        """
        """ Custom print display for class and instance objects """
        return "Instance of <class {}> at: {}".format(
            self.__class__.__name__, hex(id(self))
        )


# ==============================================================================
# singleton objects
# ==============================================================================
class Singleton(object):
    """
    Class object that generates a single instance object.

    If an instance object has been created from this class object
    subsequent class instantiation calls will return the previous
    instance object
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Called to create a new instance of class cls. __new__()

        :param cls: the class object being instantiated
        :type cls: instance of 
        :param *args: positional parameters passed to cls.__init__()
        :type *args: tuple
        :param **kwargs: keyword parameters passed to cls.__init__()
        :type **kwargs: dict
        :return: new instance of cls
        :rtype: instance of 
        """
        # hand back previous instance object
        if cls._instance:
            return cls._instance

        # create new instance object
        cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class Overwriter(object):
    """
    Class object that generates a single instance object.

    If an instance object has been created from this class object
    subsequent class instantiation calls will return delete the
    previous instance object and generate a new one
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Called to create a new instance of class cls. __new__()

        :param cls: the class object being instantiated
        :type cls: instance of 
        :param *args: positional parameters passed to cls.__init__()
        :type *args: tuple
        :param **kwargs: keyword parameters passed to cls.__init__()
        :type **kwargs: dict
        :return: new instance of cls
        :rtype: instance of
        """
        # delete previous instance
        for name, obj in globals().iteritems():
            if obj is None:
                continue

            if obj == cls._instance:
                globals().pop(name)
                del(obj)
                break

        # create new instance object
        cls._instance = super(Overwriter, cls).__new__(cls, *args, **kwargs)
        return cls._instance
