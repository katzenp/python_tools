"""
data_structures.py

Description:
    Basic data structure objects
"""


class Node(object):
    """
    Object representing a single node in hierarchy.

    Public Attributes:
        attr1:
    """
    def __init__(self, name, parent=None):
        """
        Initializes this object'properties

        :param name: this object's name
        :type name: string
        :param parent: this object's parent
        :type parent: instance of <class 'Node'> or <type 'NoneType'>
        :return: n/a
        :rtype: n/a
        """
        self.name = name
        self.parent = parent
        self._children = []

    # --------------------------------------------------------------------------
    # general
    # --------------------------------------------------------------------------
    @property
    def index(self):
        """
        Returns this nodes inex relative to its parent

        :return: int
        :rtype: int
        """
        if self._parent is not None:
            return self._parent._children.index(self)
        return 0

    @property
    def long_name(self):
        """
        Returns a pipe separated string representing the full hierarchical
        path to this object

        :return: this object's full hierarchical name
        :rtype: string
        """
        accumulator = []
        self._accumulate_ancestors(accumulator)
        accumulator.insert(0, "")
        return "|".join(accumulator)

    def draw_hierarchy(self, indent=0):
        """
        Prints out/displays the descendants of this object like:
            self
            |-- child
            `-- child

        :param indent: how much to indent each child in the the hierarchy
        :type indent: int
        :return: n/a
        :rtype: n/a
        """
        branch = ""
        if self.parent:
            branch = "|-- "
            if self is self.parent._children[-1]:
                branch = "`-- "
        line = "{istr:<{indent}}{branch}{name}".format(
            istr="", indent=indent, branch=branch, name=self
        )
        print(line)
        for each in self._children:
            each.draw_hierarchy(indent+2)

    # --------------------------------------------------------------------------
    # children
    # --------------------------------------------------------------------------
    @property
    def children(self):
        """
        Returns a list of this object's children

        :return: this node's children
        :rtype: list
        """
        return self._children

    @property
    def child_count(self):
        """
        Returns the number of children associated with this object

        :return: the number of children associated with this object
        :rtype: int
        """
        return len(self._children)

    def child(self, index):
        """
        Returns this object's child located at the given index

        :param index: list index of the child you wish to fetch
        :type index: int
        :return: this object's child located at the given index
        :rtype: instance of <class 'Node'>
        """
        return self._children[index]

    def append(self, object_):
        """
        Adds the given object to the end of this object's children list

        :param object_: the object to add
        :type object_: instance of <class 'Node'>
        :return: n/a
        :rtype: n/a
        """
        self._children.append(object_)

    def insert(self, index, object_):
        """
        Inserts the given object into this object's children lost at the given index

        :param index: the index to insert at
        :type index: int
        :param object_: the object to insert
        :type object_: instance of <class 'Node'>
        :return: n/a
        :rtype: n/a
        """
        self._children.insert(index, object_)

    def remove(self, object_):
        """
        Removes the specified object from this object's children list

        :param object_: the object to remove
        :type object_: any
        :return: n/a
        :rtype: n/a
        """
        self._children.remove(object_)
        object_.parent = None

    def pop(self, index=None):
        """
        Removes this node's child object at the given index and returns it.

        :param index: index of the child to remove
        :type index: int
        :return: the child object that got removed
        :rtype: instance of <class "Node'>
        """
        if index is None:
            index = self.child_count - 1
        object_ = self._children.pop(index)
        object_.parent = None
        return object_

    # --------------------------------------------------------------------------
    # descendants
    # --------------------------------------------------------------------------
    def _accumulate_descendants(self, accumulator):
        """
        Collects all descendants of this object into the given `accumulator` object

        :param accumulator: object used to store any relevant values
        :type accumulator: list, dict
        :return: n/a
        :rtype: n/a
        """
        for each in self._children:
            if isinstance(accumulator, list):
                accumulator.append(each)
                each._accumulate_descendants(accumulator)
            elif isinstance(accumulator, dict):
                accumulator[each] = {}
                if not each.child_count:
                    accumulator[each] = []
                each._accumulate_descendants(accumulator[each])

    def descendants(self, as_list=True):
        """
        Returns all of this object's descendants as either a list or a dictionary

        :param as_list: option to return a list
        :type as_list: bool
        :return: of this object's descendants
        :rtype: list, dict
        """
        accumulator = {}
        if as_list: 
            accumulator = []
        self._accumulate_descendants(accumulator)
        return accumulator

    # --------------------------------------------------------------------------
    # ancestors
    # --------------------------------------------------------------------------
    @property
    def parent(self):
        """
        Returs this object's parent

        :return: this object's parent
        :rtype: instance of <class 'Node'> or <type 'NoneType'>
        """
        return self.__dict__.get("parent")

    @parent.setter
    def parent(self, object_):
        """
        Sets this object's parent to the given object_
        If `object_` is None, this object will be unparented

        :param object_: this object's new parent
        :type object_: instance of <class 'Node'> or <type 'NoneType'>
        :return: n/a
        :rtype: n/a
        """
        if object_ in self._children:
            raise RuntimeError("Hierarchy cycle error !")

        # unlink from current parent
        cur_parent = self.__dict__.get("parent")
        if cur_parent is not None:
            cur_parent.children.remove(self)

        # link to new parent
        self.__dict__["parent"] = object_
        if object_ is not None:
            object_.append(self)

    def _accumulate_ancestors(self, accumulator):
        """
        Collects all ancestors of this object into the given `accumulator` object

        :param accumulator: object used to store any relevant values
        :type accumulator: list, dict
        :return: n/a
        :rtype: n/a
        """
        parent = self.parent
        if parent is not None:
            if isinstance(accumulator, list):
                accumulator.insert(0, parent)
                parent._accumulate_ancestors(accumulator)
            elif isisntance(accumulator, dict):
                new_accumulator = {self: accumulator}
                parent._accumulate_ancestors(new_accumulator)

    def ancestors(self, as_list=True):
        """
        Returns all of this object's ancestors as either a list or a dictionary

        :param as_list: option to return a list
        :type as_list: bool
        :return: of this object's ancestors
        :rtype: list, dict
        """
        accumulator = {}
        if as_list:
            accumulator = []
        self._accumulate_ancestors(accumulator)
        return accumulator

    # --------------------------------------------------------------------------
    # operators
    # --------------------------------------------------------------------------
    def __repr__(self):
        """
        Return a string that can be used to re-generate this object

        :return: string that can be used to re-generate this object
        :rtype: string
        """
        msg = "{cls}(name={name}, parent={parent})".format(
            cls=self.__class__.__name__, name=self.name, parent=self.parent
        )
        return msg

    def __str__(self):
        """
        Returns this node's name

        :return: this node's name
        :rtype: string
        """
        return self.name

    def __contains__(self, object_):
        """
        Returns a boolean value signifying if the given object is a child of this object

        :param object_: the object to evaluate
        :type object_: any
        :return: if the given object is a child of this object
        :rtype: bool
        """
        for each in self._children:
            if each is object_:
                return True
        return False


class LinkedNode(object):
    """
    Simple object representing a single node within a chain of linked nodes.

    Public Attributes:
        attr1:
    """

    def __init__(self, data):
        """
        Constructor method

        :param data: the object that this LinkedNode refers to
        :type data: any object
        :return: N/A
        :rtype: N/A
        """
        self._data = data
        self._next = None

    @property
    def data(self):
        """
        Returns this nodes data

        :return: N/A
        :rtype: N/A
        """
        return self._data

    @property
    def next(self):
        """
        Returns the next object

        :return: the next object
        :rtype: instance of <class 'LinkedNode'>
        """
        return self._next

    def setData(self, newData):
        """
        Sets this LinkedNode to the given object

        :param newData: the object you want this LinkedNode to represent
        :type newData: any object
        :return: N/A
        :rtype: N/A
        """
        self._data = newData

    def setNext(self, newNext):
        """
        Specifies which LinkedNode follows this one

        :param newNext: the next node in the chain
        :type newNext: instance of <class 'LinkedNode'>
        :return: N/A
        :rtype: N/A
        """
        if not isinstance(newNext, LinkedNode):
            type_a = type(self)
            type_b = type(newNext)
            msg = 'Invalid object type. Expected {0}. Got {2}'.format(type_a, type_b)
            raise TypeError(msg)
        self._next = newNext


class Stack(object):
    """
    Simple stack object representing a FILO data structure
    where items are added to /removed from the top of the stack

    Public Attributes:
        attr1:
    """

    def __init__(self):
        """
        Constructor method

        :return: N/A
        :rtype: N/A
        """
        self._data = []

    @property
    def data(self):
        """
        Allows you to view the Stack data

        :return: N/A
        :rtype: N/A
        """
        return self._data

    def push(self, item):
        """
        Adds the given item to the top of the stack

        :param item: the item to add to the stack
        :type item: any valid object
        :return: N/A
        :rtype: N/A
        """
        self._data.append(item)

    def pop(self):
        """
        Removes and returns the top item in the stack

        :return: the top item in the stack
        :rtype: any object
        """
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        """
        Returns the top item in the stack

        :return: the top item in the stack
        :rtype: any object
        """
        if self._data:
            return self._data[-1]
        return None

    def isEmpty(self):
        """
        Returns the emptiness status of this stack

        :return: if this stack is empty or not
        :rtype: bool
        """
        return self._data == []

    def size(self):
        """
        Returns the number of items currently in the stack

        :return: number of items in the stack
        :rtype: int
        """
        return len(self._data)


class Queue(object):
    """
    Simple queue object representing a FIFO data structure
    where index -1 is the front of the line and items are added to the end
    and removed from the front

    Public Attributes:
        attr1:
    """

    def __init__(self):
        """
        Constructor method

        :return: N/A
        :rtype: N/A
        """
        self._data = []

    @property
    def data(self):
        """
        Allows you to view the Stack data

        :return: N/A
        :rtype: N/A
        """
        return self._data

    def enqueue(self, item):
        """
        Adds the given item to the end of the queue

        :param item: the item to add to the queue
        :type item: any object
        :return: N/A
        :rtype: N/A
        """
        self._data.insert(0, item)

    def dequeue(self):
        """
        Removes and returns the first item in the queue

        :return:
        :rtype:
        """
        if self._data:
            return self._data.pop()
        return None

    def isEmpty(self):
        """
        Returns the emptiness status of this stack

        :return: if this stack is empty or not
        :rtype: bool
        """
        return self._data == []

    def size(self):
        """
        Returns the number of items currently in the stack

        :return: number of items in the stack
        :rtype: int
        """
        return len(self._data)


class Deque(object):
    """
    Simple double ended queue object representing a double ended data structure
    where index -1 is the front of the queue and items can be added/removed
    either end

    Public Attributes:
        attr1:
    """

    def __init__(self):
        """
        Constructor method

        :return: N/A
        :rtype: N/A
        """
        self._data = []

    @property
    def data(self):
        """
        Allows you to view the Stack data

        :return: N/A
        :rtype: N/A
        """
        return self._data

    def addFront(self, item):
        """
        Adds the given item to the front of the queue

        :param item: the item to add
        :type item: any object
        :return: N/A
        :rtype: N/A
        """
        self._data.append(item)

    def addRear(self, item):
        """
        Adds the given item to the end of the queue

        :param item: the item to add
        :type item: any object
        :return: N/A
        :rtype: N/A
        """
        self._data.insert(0, item)

    def removeFront(self):
        """
        Removes and returns the first item in the queue

        :return: first item in the queue
        :rtype: any object
        """
        if self._data:
            return self._data.pop()
        return None

    def removeRear(self):
        """
        Removes and returns the last item in the queue

        :return: last item in the queue
        :rtype: any object
        """
        if self._data:
            return self._data.pop(0)
        return None

    def isEmpty(self):
        """
        Returns the emptiness status of this stack

        :return: if this stack is empty or not
        :rtype: bool
        """
        return self._data == []

    def size(self):
        """
        Returns the number of items currently in the stack

        :return: number of items in the stack
        :rtype: int
        """
        return len(self._data)


class UnorderedList(object):
    """
    Unordered list type.
    Each item in the list is represented by an instance of <class 'LinkedNode'>
    which contains a reference to the next item in the list.
    The head of the list is always the most recent item added and the tail of
    the list always has an item whose next item is None

    Public Attributes:
        attr1:
    """
    def __init__(self):
        self._head = None
        self._length = 0

    @property
    def length(self):
        """
        Returns the number of items in this list

        :return: number of items in this list
        :rtype: int
        """
        return self._count

    def add(self, item):
        """
        Adds an item to the head of the list

        :param item: the item to add.
        :type item: any. Will get converted into an instance of <class 'LinkedNode'>
        :return: N/A
        :rtype: N/A
        """
        node = LinkedNode(item)
        node.setNext(self._head)
        self._head = node
        self._length += 1

    def remove(self, item):
        """
        Removes the given item from the list

        :param item: the item to remove
        :type item: instance of <class 'LinkedNode'
        :return: N/A
        :rtype: N/A
        """
        # find the node
        previous_node = None
        current_node = self._head
        while current_node:
            # found it
            if current_node.data == item:
                if previous_node is None:
                    self._head = current_node.next
                else:
                    previous_node.setNext(current_node.next)
                self._length -= 1
                break
            # keep looking
            previous_node = current_node
            current_node = current_node.next

    def search(self, item):
        """
        Looks for the first occurence of the given item

        :param item: the item to search for
        :type item: instance of <class 'LinkedNode'>
        :return: wether or not the item is in the list
        :rtype: bool
        """
        current_node = self._head
        while current_node:
            if current_node.data == item:
                return True
            current_node = current_node.next
        return False

    def isEmpty(self):
        """
        Returns if this list is empty or not

        :return: if the list is empty or not
        :rtype: bool
        """
        return self._head is None

    def append(self, item):
        """
        Adds an item to the tail of the list

        :param item:
        :type item:
        :return:
        :rtype:
        """
        # get the last node in the list
        last_node = self._head
        while last_node:
            last_node = last_node.next

        # replace the last node
        node = LinkedNode(item)
        if last_node is None:
            node.setNext(self.head)
            self._head = node
        else:
            last_node.setNext(node)
        self._length += 1

    def index(self, item):
        """
        Tries to get the index of the given item

        :param item: the item to search for
        :type item: instance of <class 'LinkedNode'>
        :return: the items index value, if found. None otherwise
        :rtype: int, None
        """
        index = 0
        current_node = self._head
        while current_node:
            if current_node.data == item:
                return index
            current_node = current_node.next
            index += 1
        raise IndexError('list index out of range')

    def insert(self, index, item):
        """
        Inserts the given item at the specified index

        :param index:
        :type index:
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # iterate to index
        if index > (self._length - 1) or index < 0:
            raise IndexError('list index out of range')

        # get the node currently at the index
        current_node = self.head
        while count < index:
            current_node = current_node.next
        for i in range(index):
            print(i)

        # replace index with current item

    def pop(index=None):
        pass
