"""
qt_lib.py

Description:
   Python Qt objects and utilities
"""
# stdlib
import sys

# external
from PyQt5 import QtCore, QtGui, QtWidgets

# internal
import python_tools.arithmetic as arithmetic
from python_tools.data_structures import Node


# ==============================================================================
# constants/globals
# ==============================================================================
Q_OBJ_TYPE = type(QtCore.QObject)


# =============================================================================
# general
# =============================================================================
def get_app():
    """
    Fetches or creates a QApplication

    :return:
    :rtype:
    """
    app = QtCore.QCoreApplication.instance()
    if not app:
        app = QtCore.QCoreApplication(sys.argv)
    return app


# ==============================================================================
# ui launch - singleton mode
# ==============================================================================
def get_ui(cls, *args, **kwargs):
    """
    Returns a new instance of the given ui class ui ensuring that that there is
    only ever one instance in existence at a time. Forces singleton like behavior
    for the given ui class

    :param cls: name of the ui class whose instances you wish to manage
    :type cls: any ui object type
    :param *args: positional parameters passed to cls.__init__
    :type *args: tuple
    :param **kwargs: keyword parameters passed to cls.__init__
    :type **kwargs: dict
    :return: the ui instance being created
    :rtype: any ui object type
    """
    # remove class instances from global symbols table
    remove = []
    for name, obj in sorted(globals().iteritems()):
        if isinstance(obj, cls):
            remove.append(name)
            print("deleting: {}".format(obj))
            try:
                obj.close()
                if not obj.testAttribute(QtCore.Qt.WA_DeleteOnClose):
                    obj.destroy()
            except Exception:
                pass
    # clean up global symbold table
    map(globals().pop, remove)

    # make new global symbol/object
    key = "{}_obj".format(cls.__class__.__name__)
    ui_obj = cls(*args, **kwargs)
    globals()[key] = ui_obj

    return ui_obj


class Singleton_Ui_Meta(Q_OBJ_TYPE, type):
    """
    Description of class < Singleton_Ui_Meta >

    Usage:
        class MyUi(QtWidgets.QDialog):
            __metaclass__ = Singleton_Ui_Meta

            def __init__(self, title="test", parent=None):
                super(MyUi, self).__init__(parent)
                self.setWindowTitle(title)   

    Public Attributes:
        attr1:
    """
    _instance = None
    def __new__(cls, name, bases, kwargs):
        return super(Singleton_Ui_Meta, cls).__new__(cls, name, bases, kwargs)

    def __init__(cls, name, bases, kwargs):
        super(Singleton_Ui_Meta, cls).__init__(name, bases, kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            message = "Creating a new  instance of {class_obj}".format(class_obj=cls)
            print(message)
            cls._instance = super(Singleton_Ui_Meta, cls).__call__(*args, **kwargs)
        else:
            message = "An instance of {class_obj} already exists !".format(class_obj=cls)
            print(message)
        return cls._instance


# ==============================================================================
# model/view objects
# ==============================================================================
class ListModel(QtCore.QAbstractListModel):
    """
    Generic list model object for the Python Qt Model/View architecture.
    The data block for this model is a list

    Public Attributes:
        :attr block: list of objects that defines this model's internal data block
        :type block: list
    """
    def _init__(self, parent=None):
        """
        Defines and initializes each instance object

        :param block: list of objects that defines this model's internal data block
        :type block: list, tuple
        :param editable: this models editable state
        :type editable: bool
        :param parent: this widget's parent
        :type parent: instance of <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(ListModel, self).__init__(parent)
        self.block = []

    # --------------------------------------------------------------------------
    # managed attributes
    # --------------------------------------------------------------------------
    @property
    def block(self):
        """
        Returns the list of objects that defines this model's internal data block

        :return: list of objects that defines this model's internal data block
        :rtype: list
        """
        return self.__dict__.get("block")

    @block.setter
    def block(self, value):
        """
        Defines the list of objects that make up this model's internal data block

        :param value: list of objects
        :type value: list
        :return: n/a
        :rtype: n/a
        """
        if not isinstance(value, list):
            raise TypeError("data block MUST be an instance of <type \'list\'>")
        self.__dict__["block"] = value

    # --------------------------------------------------------------------------
    # super-class overrides
    # --------------------------------------------------------------------------
    def rowCount(self, parent):
        """
        Returns the number of items in the internal data block

        :param parent: parent of the QModelIndex being operated on
        :type parent: instance of <class 'QModelIndex'>
        :return: number of rows that this model defines
        :rtype: int
        """
        return len(self.block)

    def columnCount(self, parent):
        """
        Returns the number of columns

        :param parent: parent of the QModelIndex being operated on
        :type parent: instance of <class 'QModelIndex'>
        :return: number of columns that this model defines
        :rtype: int
        """
        return 1

    def flags(self, index):
        """
         Sets the various properties of a QModelIndex

        :param index: The QModelIndex whose properties you wish to set
        :type index: instance of <class 'QModelIndex'>
        :return: aggregated item property flags
        :rtype: QtCore.Qt.ItemFlag attributes
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def data(self, index, role):
        """
        Returns QModelIndex display data based on the requested display role

        :param index: The QModelIndex whose data yopu wish to fetch
        :type index: instance of <class 'QModelIndex'>
        :param role: a Qt.ItemDataRole specifying the type of data the view is requesting
        :type role: Qt.ItemDataRole
        :return: data that informs a view object how to display a QModelIndex 
        :rtype: various
        """
        row = index.row()
        if role == QtCore.Qt.DisplayRole:
            return self.block[row]

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Sets the given QModelIndex's display data to the given value for the specified role

        :param index: The QModelIndex to operate on
        :type index: instance of <class 'QModelIndex'>
        :param value: QObject/data associated with the specified role
        :type value: various
        :param role: a Qt.ItemDataRole specifying the type of data the view is requesting
        :type role: Qt.ItemDataRole
        :return: boolean value representing success of the operation
        :rtype: bool
        """
        # check that model is editable
        if not self.editable:
            return False

        # edit the main data set
        row = index.row()
        value = value.toString()
        if role == QtCore.Qt.EditRole:
            self.block[row] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def index(self, row, column, parent):
        """
        Returns the QModelIndex associated with the given row and column

        :param row: The row number
        :type row: int
        :param column: Then column number
        :type column: int
        :return: the parent of the the given QModelIndex
        :rtype: instance of <class 'QModelIndex'>
        """
        dataItem = self.block[row]
        index = self.createIndex(row, column, dataItem)
        return index

    def parent(self, index):
        """
        Returns the parent of the the given QModelIndex

        :param index: the QModelInedx whose parent you wish to fetch
        :type index: instance of <class 'QModelIndex'>
        :return: the parent of the the given QModelIndex
        :rtype: instance of <class 'QModelIndex'>
        """
        return QtCore.QModelIndex()

    def insertRow(self, position, parent=QtCore.QModelIndex()):
        """
        Inserts a row into the model at the given position.

        Note:
            MUST call self.beginInsertRows(index, first, last)
            first is the start index
            last is the final index number

        :param position: The list index to insert at
        :type position: int
        :param parent: parent of the QModelIndex being operated on
        :type parent: instance of <class 'QModelIndex'>
        """
        # check that model is editable
        if not self.editable:
            return False

        self.beginInsertRows(parent, position, position)
        newData = ''
        self.block.insert(position, newData)
        self.endInsertRows()
        return True

    def insertRows(self, position, count, parent=QtCore.QModelIndex()):
        """
        Inserts rows into the model at the given position.

        Note:
            MUST call self.beginInsertRows(index, first, last)
            first is the start index
            last is the final index number

        :param position: The list index to insert at
        :type position: int
        :param count: number of rows to insert
        :type count: int
        :param parent: parent of the QModelIndex being operated on
        :type parent: instance of <class 'QModelIndex'>
        """
        # check that model is editable
        if not self.editable:
            return False

        last = position + (count - 1)
        self.beginInsertRows(parent, position, last)
        for i in xrange(count):
            newData = ''
            self.block.insert(position, newData)
        self.endInsertRows()
        return True

    def removeRow(self, position, parent=QtCore.QModelIndex()):
        """
        Removes a row from the model at the given position.

        Note:
            MUST call self.beginInsertRows(index, first, last)
            first is the start index
            last is the final index number

        :param position: The list index to remove
        :type position: int
        :param parent: parent of the QModelIndex being operated on
        :type parent: instance of <class 'QModelIndex'>
        """
        # check that model is editable
        if not self.editable:
            return False

        self.beginRemoveRows(parent, position, position)
        self.block.pop(position)
        self.endRemoveRows()
        return True

    def removeRows(self, position, count, parent=QtCore.QModelIndex()):
        """
        Removes rows from the model at the given position.

        Note:
            MUST call self.beginInsertRows(index, first, last)
            first is the start index
            last is the final index number

        :param position: The list index to begin removing from
        :type position: int
        :param count: number of rows to remove
        :type count: int
        :param parent: parent of the QModelIndex being operated on
        :type parent: instance of <class 'QModelIndex'>
        """
        # check that model is editable
        if not self.editable:
            return False

        last = position + (count - 1)
        self.beginRemoveRows(parent, position, last)
        for i in xrange(count):
            self.block.pop(position)
        self.endRemoveRows()
        return True


class TableModel(QtCore.QAbstractTableModel):
    """
    Generic table model class for use with the PyQt Model/View architecture.
    The internal data block should be a list of nested lists/tuples
    """
    def __init__(self, block=[], horizontal_labels=[], vertical_labels=[], parent=None):
        """
        Defines and initializes each instance object

        :param block: The base data set
        :type block: nested lists
        :param horizontal_labels: column labels
        :type horizontal_labels: list
        :param vertical_labels: row labels
        :type vertical_labels: list
        :param parent: this model object's parent
        :type parent: instance of <class 'QtCore.QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(TableModel, self).__init__(parent)

        self._block = block
        self._horizontal_labels = horizontal_labels
        self._vertical_labels = vertical_labels

    # --------------------------------------------------------------------------
    # Managed attributes
    # --------------------------------------------------------------------------
    @property
    def block(self):
        """
        Returns this object's internat data set

        :return: this object's internat data set
        :rtype: list
        """
        return self._block

    @property
    def horizontal_labels(self):
        """
        Returns the list of column labels

        :return: column labels
        :rtype: list
        """
        return self._horizontal_labels

    @property
    def vertical_labels(self):
        """
        Returns the list of row labels

        :return: row labels
        :rtype: list
        """
        return self._vertical_labels

    # --------------------------------------------------------------------------
    # superclass overrides
    # --------------------------------------------------------------------------
    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Returns the number of number of rows this model contains

        :param parent: The QModelIndex you wish to query
        :param parent: instance of <class 'QtCore.QModelIndex'>
        :return: n/a
        :rtype: int
        """
        return len(self._block)

    def columnCount(self, parent=QtCore.QModelIndex()):
        """
        Returns the number of columns number of columns this model contains

        :param parent: The QModelIndex you wish to query
        :param parent: instance of <class 'QtCore.QModelIndex'>
        :return: number of columns this model contains
        :rtype: int
        """
        try:
            return len(self._block[0])
        except IndexError:
            return 1

    def flags(self, index):
        """
        Sets the various properties of QModelIndex objects associated with this model

        :param index: The QModelIndex to operate on
        :param index: instance of <class 'QtCore.QModelIndex'>
        :return: item data flags
        :rtype: QtCore.Qt.ItemData flag
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def data(self, index, role):
        """
        Returns a value that this model's view expects for the specified role

        :param index: The QModelIndex to operate on
        :param index: instance of <class 'QtCore.QModelIndex'>
        :param role: the item data role whose value you wish to fetch
        :type role: QtCore.Qt.ItemDataRole value
        :return: a piece of data from the internal data block
        :rtype: any
        """
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._block[row][column]
            return value

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Updates the internal data block and notifies this model's view that there
        is new data to display 

        :param index: The QModelIndex to operate on
        :param index: instance of <class 'QtCore.QModelIndex'>
        :param value: The value to set
        :param value: instance of <class 'QtCore.QVariant'>
        :return: success status of the operation
        :rtype: bool
        """
        # edit the main data set
        row = index.row()
        column = index.column()
        value = value.toString()
        if role == QtCore.Qt.EditRole:
            self._block[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        """
        Returns a value that this model's header views expect for the specified role

        :param section: The row/column to operate on
        :type section: int
        :param orientation: the header object's orientation
        :type orientation: {QtCore.Qt.Horizontal, QtCore.Qt.Vertical}
        :param role: the item data role whose value you wish to fetch
        :type role: QtCore.Qt.ItemDataRole value
        :return: a piece of data from the internal data block
        :rtype: any
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                try:
                    return self._horizontal_labels[section]
                except IndexError:
                    return ''
            elif orientation == QtCore.Qt.Vertical:
                try:
                    return self._vertical_labels[section]
                except IndexError:
                    return ''

    def insertRow(self, position, parent=QtCore.QModelIndex()):
        """
        Inserts a single row into this model object's internal data block

        Note:
            Must call self.beginInsertRows(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to insert at
        :type position: int
        :param parent: the row's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def insertRows(self, position, count, parent=QtCore.QModelIndex()):
        """
        Inserts multiple rows into this model object's internal data block

        Note:
            Must call self.beginInsertRows(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to insert at
        :type position: int
        :param count: How many rows to insert
        :type count: int
        :param parent: the row's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def insertColumn(self, position, parent=QtCore.QModelIndex()):
        """
        Inserts a single column into this model object's internal data block

        Note:
            Must call self.beginInsertColumns(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to insert at
        :type position: int
        :param parent: the column's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def insertColumns(self, position, count, parent=QtCore.QModelIndex()):
        """
        Inserts multiple columns into this model object's internal data block

        Note:
            Must call self.beginInsertColumns(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to insert at
        :type position: int
        :param count: How many columns to insert
        :type count: int
        :param parent: the row's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def removeRow(self, position, parent=QtCore.QModelIndex()):
        """
        Removes a single row into this model object's internal data block

        Note:
            Must call self.beginRemoveRows(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to remove from
        :type position: int
        :param parent: the row's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def removeRows(self, position, count, parent=QtCore.QModelIndex()):
        """
        Removes multiple rows into this model object's internal data block

        Note:
            Must call self.beginRemoveRows(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to remove from
        :type position: int
        :param count: number of rows to remove
        :type count: int
        :param parent: the row's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def removeColumn(self, position, parent=QtCore.QModelIndex()):
        """
        Removes a single column from this model object's internal data block

        Note:
            Must call self.beginRemoveColumns(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to remove from
        :type position: int
        :param parent: the column's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()

    def removeColumns(self, position, count, parent=QtCore.QModelIndex()):
        """
        Removes multiple columns from this model object's internal data block

        Note:
            Must call self.beginRemoveColumns(index, first, last)
            where first is the start index, and last is the final index number

        :param position: The list index to remove from
        :type position: int
        :param count: number of columns to remove
        :type count: int
        :param parent: the column's parent index object
        :type parent: instance of <class 'QtCore.QModelIndex'>
        :return: success status of the operation
        :rtype: bool
        """
        raise NotImplementedError()


class TreeModel(QtCore.QAbstractItemModel):
    """
    QAbstractItemModel object representing generic hierarchical data.
    The Node instance associated with attribute "root" represents a container object
    which can be used to gather all relevant information about the current
    variant hierarchy defined by this model
    For more information please consult the Node class documentation in this module

    Public Attributes:
        :attr root: the root node of the variant hierarchy defined by this model
        :type root: instance of <class 'Node'>
    """
    def __init__(self, root=None, parent=None):
        """
        Defines and initializes each instance object

        :param parent: this widget's parent
        :type parent: instance of <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(TreeModel, self).__init__(parent)
        self._root = Node("root")

    # --------------------------------------------------------------------------
    # managed attributes
    # --------------------------------------------------------------------------
    @property
    def root(self):
        """
        Returns the root node of the variant hierarchy defined by this model

        :return: the root node of the variant hierarchy defined by this model
        :rtype: instance of <class 'Node'>
        """
        return self._root

    @root.setter
    def root(self, value):
        """
        Returns the root node of the variant hierarchy defined by this model

        :return: the root node of the variant hierarchy defined by this model
        :rtype: instance of <class 'Node'>
        """
        if not isinstance(value, Node):
            msg = "Invalid root node. Expected {} - got {}".format(type(Node), type(value))
            raise TypeError(msg)
        self.__dict__["_root"] = value

    # --------------------------------------------------------------------------
    # general
    # --------------------------------------------------------------------------
    def _get_node(self, index):
        """
        Returns the instance of <class 'Node'> associated with the given QModelIndex

        :param index: the QModelIndex to operate on
        :type index: instance of <class 'QModelIndex'>
        :return: the instance of <class 'Node'> associated with the given QModelIndex
        :rtype: instance of <class 'Node'>
        """
        if index and index.isValid():
            return index.internalPointer()
        return self._root

    # --------------------------------------------------------------------------
    # super-class overrides
    # --------------------------------------------------------------------------
    def rowCount(self, index=QtCore.QModelIndex()):
        """
        Returns the number of children associated with the specified QModelIndex

        :param index: the QModel index to query
        :type index: instance of <class 'QModelIndex'>
        :return: number of children
        :rtype: int
        """
        node = self._root
        if index and index.isValid():
            node = index.internalPointer()
        return node.child_count

    def columnCount(self, index=QtCore.QModelIndex()):
        """
        Returns the number of objects associated with the children
        of the specified QModelIndex

        :param index: the QModel index to query
        :type index: instance of <class 'QModelIndex'>
        :return: number of data objects
        :rtype: int
        """
        return 1

    def flags(self, index):
        """
        Defines various properties of the specified QModelIndex.

        :param index: the QModel index to operate on
        :type index: instance of <class 'QModelIndex'>
        :return: aggregated ItemDataFlags
        :rtype: QtCore.Qt.ItemDataFlags
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def data(self, index, role):
        """
        Returns an appropriate value for the role that the view is requesting

        :param index: the QModelIndex representing the view data to fetch
        :type index: instance of <class 'QModelIndex'>
        :param role: a role indicating the type of data the view is requesting
        :type role: Qt.ItemDataRole constant
        :return: a view role specific value
        :rtype: various
        """
        if not index.isValid() or index.column() > self.columnCount():
            return None

        # text
        if role == QtCore.Qt.DisplayRole:
            node = index.internalPointer()
            return node.name

        # font
        if role == QtCore.Qt.FontRole:
            return QtGui.QFont("Arial", 8, QtGui.QFont.Normal)

        # color
        if role == QtCore.Qt.ForegroundRole:
            return QtGui.QColor(220, 220, 220)

        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Updates the internal data block and notifies this model's view that there
        is new data to display

        :param index: The QModelIndex to operate on
        :param index: instance of <class 'QtCore.QModelIndex'>
        :param value: The value to set
        :param value: instance of <class 'QtCore.QVariant'>
        :param role: a role indicating the type of data the view is requesting
        :type role: Qt.ItemDataRole constant
        :return: success status of the operation
        :rtype: bool
        """
        # check if we should be editing
        if role != QtCore.Qt.EditRole:
            return False

        # perform edit
        node = index.internalPointer()
        if value:
            node.name = value
            self.dataChanged.emit(index, index)
            return True

        return False

    def headerData(self, section, orientation, role):
        """
        Returns an appropriate value for the role that the header view is requesting

        :param section: the row or column number being requested
        :type section: int
        :param orientation: the header view orientation - (Qt.Horizontal, Qt.Vertical
        :type orientation: Qt.Orientation constant
        :param role: a role indicating the type of data the view is requesting
        :type role: Qt.ItemDataRole constant
        :return: a view role specific value
        :rtype: various
        """
        if orientation == QtCore.Qt.Vertical or section != 0:
            return None

        # text
        if role == QtCore.Qt.DisplayRole:
            text = "Column{}".format(section)
            if orientation == QtCore.Qt.Vertical:
                text = "Row{}".format(section)
            return text

        # font
        if role == QtCore.Qt.FontRole:
            return QtGui.QFont("Arial", 8, QtGui.QFont.Bold)

        # color
        if role == QtCore.Qt.ForegroundRole:
            return QtGui.QColor(220, 220, 220)

        return None

    def parent(self, index):
        """
        Returns the parent of the specified QModelIndex

        :param index: the QModelIndex to operate on
        :type index: instance of <class 'QModelIndex'>
        :return: the parent of the specified QModelIndex
        :rtype: instance of <class 'QModelIndex'>
        """
        node = self._get_node(index)
        parent_node = node.parent
        if parent_node == self._root:
            return self.createIndex(-1, -1, parent_node)
        return self.createIndex(index.row(), 0, parent_node)

    def createIndex(self, row, column, object_):
        """
        Creates a QModelIndex object for the specified row and column
        that is associated with the given object

        :param row: the row number
        :type row: int
        :param column: the column number
        :type column:  int
        :param object_: the object the QModelIndex is associalted with
        :type object_: any
        :return:
        :rtype: instance of <class 'QModelIndex'>
        """
        return super(TreeModel, self).createIndex(row, column, object_)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        """
        Returns a QModelIndex for the given row and column, with the specified parent

        :param row: the child index's row number relative to the specified parent index
        :type row: int
        :param column: the child index's column number relative to the specified parent index
        :type column: int
        :param parent: QModelIndex whose child index you wish to fetch
        :type parent: instance of <class 'QModelIndex'>
        :return: child index
        :rtype: instance of <class 'QModelIndex'>
        """
        # get Node object
        parent_node = self._get_node(parent)
        child_node = parent_node.child(row)

        # create QModelIndex
        index = self.createIndex(-1, -1, self._root)
        if child_node:
            index = self.createIndex(row, column, child_node)
        return index

    def insertRows(self, row, count=1, parent=QtCore.QModelIndex()):
        # get parent node
        parent_node = self._root
        if parent and parent.isValid():
            parent_node = parent.internalPointer()

        # update QModelIndex hierarchy
        self.beginInsertRows(parent, row, row + count)
        for i in range(count):
            name = "child{}".format(i)
            child_node = Node(name, parent=parent_node)
            self.createIndex(row, 0, child_node)
            row += i
        self.endInsertRows()

        return True

    def removeRows(self, row, count=1, parent=QtCore.QModelIndex()):
        # update QModelIndex hierarchy
        self.beginRemoveRows(parent, row, row + count)
        for i in range(row, row + count):
            child_node = parent.child(i, 0).internalPointer()
            child_node.parent = None
        self.endRemoveRows()

        return True


# ==============================================================================
# custom widget/objects
# ==============================================================================
class TreeItem(QtWidgets.QTreeWidgetItem):
    """
    QTreeWidgetItem object containing convenience methods for fetching
    hierarchical information such as ancestors and descendants.

    Public Attributes:
        :attr get_ancestors(accumulator): method that recursively fetches all ancestors of this object
        :rtype get_ancestors: n/a
        :attr ancestors: a list of this object's ancestors in root to leaf order
        :rtype ancestors: list
        :attr get_descendants(accumulator): method that recursively fetches all descendants of this object
        :rtype get_descendants: n/a
        :attr descendants: a list of this object's desendants in root to leaf order
        :rtype descendants: list
        :attr children: a list of this object's immediate children
        :rtype children: list
        :attr relatives(descendants): method that returns a list of this object's descendants or ancestors in root to leaf order
        :rtype relatives: list
    """
    def __init__(self, *args, **kwargs):
        super(TreeItem, self).__init__(*args, **kwargs)

    # --------------------------------------------------------------------------
    # ancestors
    # --------------------------------------------------------------------------
    def get_ancestors(self, accumulator):
        """
        Fetches all ancestors of this node and stores them in the specified collector object

        :param accumulator: object used to collect values
        :type accumulator: list
        :return: n/a
        :rtype: n/a
        """
        parent = self.parent()
        if parent:
            if isinstance(accumulator, list):
                accumulator.insert(0, parent)
                parent.get_ancestors(accumulator)
            elif isinstance(accumulator, dict):
                new_accumulator = {self: accumulator}
                parent.get_ancestors(new_accumulator)

    @property
    def ancestors(self):
        """
        Returns a list of this object's ancestors in root to leaf order

        :return: list of this object's ancestors in root to leaf order
        :rtype: list
        """
        accumulator = list()
        self.get_ancestors(accumulator)
        return accumulator

    # --------------------------------------------------------------------------
    # descendants
    # --------------------------------------------------------------------------
    def get_descendants(self, accumulator):
        """
        Fetches all descendants of this node and stores them in the specified collector object

        :param accumulator: object used to collect values
        :type accumulator: list
        :return: n/a
        :rtype: n/a
        """
        count = self.childCount()
        for i in range(count):
            child = self.child(i)
            if isinstance(accumulator, list):
                accumulator.append(child)
                child.get_descendants(accumulator)
            elif isinstance(accumulator, dict):
                accumulator[child] = dict()
                if not child.childCount():
                    accumulator[child] = list()
                child.get_descendants(accumulator[child])

    @property
    def descendants(self):
        """
        Returns a list of this object's desendants in root to leaf order

        :return: list of this object's descendants in root to leaf order
        :rtype: list
        """
        accumulator = list()
        self.get_descendants(accumulator)
        return accumulator

    @property
    def children(self):
        """
        Returns a list of this object's immediate children

        :return: list of this object's immediate children
        :rtype: list
        """
        children = list()
        count = self.childCount()
        for i in range(count):
            children.append(self.child(i))
        return children

    # --------------------------------------------------------------------------
    # relatives
    # --------------------------------------------------------------------------
    def relatives(self, descendants=True, return_list=True):
        """
        Returns this object's descendants or ancestors in root to leaf order
        as either a list or a dictionary

        :param descendants: option to return descendants
        :type descendants: bool
        :param return_list: option to return results in a list instead of a dictionary
        :type return_list: bool
        :return: collection of this object's descendants or ancestors in root to leaf order
        :rtype: list, dict
        """
        # initialize accumulator object
        relatives = dict()
        if return_list:
            relatives = list()

        if descendants:
            self.get_descendants(relatives)
        else:
            self.get_ancestors(relatives)

        return relatives


class QCollapsableLabel(QtWidgets.QLabel):
    """
    QLabel object that can be toggled between collapsed and expanded states.
    The collapsed state is denoted by displaying a triangle pointing to the right
    The expanded state is denoted by displaying a triangle pointing down

    In addition to mouse click interaction, this widget may be expanded/collapsed
    using the set_epanded(bool) method

    Custom SIGNALS:
        toggled: emits a boolean value representing the collapsed state of the widget

    Public Attributes:
        :attr is_expanded: Returns the current expanded/collapsed state of this widget
        :type is_expanded: bool
        :attr set_expanded: sets the expanded/collapsed stat of this widget
        :type set_expanded: method
    """
    toggled = QtCore.pyqtSignal(bool)

    def __init__(self, text, height=30, parent=None):
        """
        Defines and initializes each instance object

        :param text: label text
        :type text: string
        :param height: fixed height this widget should be
        :type height: int
        :param parent: this widget's parent
        :type parent: instance on <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(QCollapsableLabel, self).__init__(text, parent)
        self.setFixedHeight(height)

        # expanded/collapsed state
        self._expanded = False

        # label text
        self._text = text

        # brush/pen
        self._palette = self.palette()
        self._painter = QtGui.QPainter(self)
        self._pen = self._painter.pen()

        # font
        self._font = self.font()
        self._text_x = height
        self._text_y = (height * .5) + (self._font.pixelSize() / 2.0)

        # colors
        self._text_color = QtGui.QColor(200, 200, 200)
        self._icon_fill_color = QtGui.QColor(200, 185, 200)
        self._icon_edge_color = self._icon_fill_color.darker(300)
        self._border_color = QtGui.QColor(45, 45, 45)

        # state display polygons
        self._poly_expanded = QtGui.QPolygonF()
        self._poly_collapsed = QtGui.QPolygonF()
        self._set_state_polygons(count=3, radius=6)

    @property
    def is_expanded(self):
        """
        Returns the current expanded/collapsed state of this widget

        :return: the current expanded/collapsed state of this widget
        :rtype: bool
        """
        return self._expanded

    def set_expanded(self, state):
        """
        Sets the expanded state of this widget and repaints it

        :param state: the new state
        :type state: bool
        :return: n/a
        :rtype: n/a
        """
        self._expanded = state
        self.repaint()

    def _set_state_polygons(self, count, radius):
        """
        Defines the polygons used for the expanded/collapsed state icon

        :param count: number of sides the polygon icon should have
        :type count: int
        :param radius: radius of the polygon shapes - defines overall icon size
        :type radius: int
        :return: n/a
        :rtype: n/a
        """
        # expanded state polygon
        cx = cy = self.height() / 2.0
        e_points = [QtCore.QPointF(*pt) for pt in arithmetic.iter_points(count=count, start_vector=(0, radius), center=(cx, cy))]
        self._poly_expanded = QtGui.QPolygonF(e_points, closed=True)

        # collapsed state polygon
        c_points = [QtCore.QPointF(*pt) for pt in arithmetic.iter_points(count=count, start_vector=(radius, 0), center=(cx, cy))]
        self._poly_collapsed = QtGui.QPolygonF(c_points, closed=True)

    # --------------------------------------------------------------------------
    # super class overrides
    # --------------------------------------------------------------------------
    def mouseReleaseEvent(self, QMouseEvent):
        """
        Defines the mouse release event for this widget.
        Emits the toggled signal

        :param QMouseEvent: mouse event being handled
        :type QMouseEvent: instance of <class 'QMouseEvent'>
        :return: n/a
        :rtype: n/a
        """
        self._expanded = not self._expanded
        self.toggled.emit(self._expanded)
        self.update()

    def paintEvent(self, paintEvent):
        """
        Defines how this widget looks

        :param paintEvent: the paint event being handled
        :type paintEvent: instance of <class 'QPaintEvent'>
        :return: n/a
        :rtype: n/a
        """
        rect = self.rect()

        self._painter.begin(self)

        # draw border
        self._pen.setWidth(2)
        self._pen.setColor(self._border_color)
        self._painter.setPen(self._pen)
        self._painter.drawRect(
            rect.x(),
            rect.y(),
            rect.width() - 1,
            rect.height() - 1)

        # draw expanded/collapsed state icon
        self._painter.setBrush(self._icon_fill_color)
        self._pen.setWidth(1)
        self._pen.setColor(self._icon_edge_color)
        self._painter.setPen(self._pen)

        poly = self._poly_collapsed
        if self._expanded:
            poly = self._poly_expanded
        self._painter.drawPolygon(poly)

        # draw text
        self._pen.setColor(self._text_color)
        self._painter.setPen(self._pen)
        self._font.setBold(True)
        self._painter.setFont(self._font)
        self._painter.drawText(self._text_x, self._text_y, self._text)

        self._painter.end()

    def sizeHint(self):
        """
        Returns the intended size of this widget

        :return: the intended size of this widget
        :rtype: instance of <class 'QSize'>
        """
        return QtCore.QSize(250, self.height())


class QCollapsableFrame(QtWidgets.QWidget):
    """
    Widget containing a header and a collapsable widget that can contain as
    many widgets as desired. The container's layout defaults to a QVBoxLayout
    unless otherwise specified during object instantiation.

    Custom SIGNALS:
        toggled: emits a boolean value representing the collapsed state of the widget
        resized: emits a QtCore.QSize object representing widgets current size

    Public Attributes:
        :attr is_expanded: returns the expanded state of this widget
        :type is_expanded: bool
        :attr set_spacing: sets the collapsable container layout's spacing
        :type set_spacing: method
        :attr set_contents_margins: sets the collapsable container layout's contents margins
        :type set_contents_margins: method
        :attr add_widget: adds a widget to the collapsable container layout
        :type add_widget: method
        :attr add_layout: adds a layout to the collapsable container layout
        :type add_layout: method
        :attr set_expanded: sets the expanded/collapsed state of this widget
        :type set_expanded: method
    """
    toggled = QtCore.pyqtSignal(bool)
    resized = QtCore.pyqtSignal(QtCore.QSize)

    STYLE_SHEET = """
    QFrame#container {
        border: 1px inset rgb(68, 68, 68);
        background-color: rgb(48, 48, 48)}
    """

    def __init__(self, header_title, header_height=30, container_layout=None, parent=None):
        """
        Defines and initializes each instance object

        :param header_title: the frame header title text
        :type header_title: string
        :param header_height: dframe header height
        :type header_height: int
        :param container_layout: the container widget's layout - defaults to QVBoxLayout
        :type container_layout: instance of <class 'QLayout'>
        :param parent: this widgets parent
        :type parent: instance of <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(QCollapsableFrame, self).__init__(parent)
        self.setStyleSheet(self.STYLE_SHEET)

        # frame header
        self._header_title = header_title
        self._header_height = header_height

        # container layout
        self._container_layout = QtWidgets.QVBoxLayout()
        self._container_layout.setSpacing(4)
        self._container_layout.setContentsMargins(4, 4, 4, 4)
        if container_layout and isinstance(container_layout, QtWidgets.QLayout):
            self._container_layout = container_layout

        # widget set up
        self._build_ui()
        self._initialize_ui()
        self._connect_signals()

    # --------------------------------------------------------------------------
    # managed attributes
    # --------------------------------------------------------------------------
    @property
    def is_expanded(self):
        """
        Returns the current expanded/collapsed state of this widget

        :return: the current expanded/collapsed state of this widget
        :rtype: bool
        """
        return self._header_label.is_expanded

    # --------------------------------------------------------------------------
    # container layout
    # --------------------------------------------------------------------------
    def set_spacing(self, value):
        """
        Sets the container widget layout spacing to the given value

        :param value: spacing value in pixels
        :type value: int
        :return:
        :rtype:
        """
        self._container_layout.setSpacing(value)

    def set_contents_margins(self, left=11, top=11, right=11, bottom=11):
        """
        Sets the container widget layout contents margins values

        :param left: the left margin value
        :type left: int
        :param top: the top margin value
        :type top: int
        :param right: the right margin value
        :type right: int
        :param bottom: the bottom margin value
        :type bottom: int
        :return: n/a
        :rtype: n/a
        """
        self._container_layout.setContentsMargins(left, top, right, bottom)

    def add_widget(self, *args, **kwargs):
        """
        Adds the specified widget to the collapsable frame widget's layout
        using the specified miscellaneous positional/keyword parameters
        appropriate to the container layout type

        :param args: miscelaneous positional parameters passed on to self._container_layout.addWidget()
        :type args: tuple
        :param args: miscelaneous keyword parameters passed on to self._container_layout.addWidget()
        :type args: tuple
        :return: n/a
        :rtype: n/a
        """
        self._container_layout.addWidget(*args, **kwargs)

    def add_layout(self, *args, **kwargs):
        """
        Adds the specified layout to the collapsable frame widget's layout
        using the specified miscellaneous positional/keyword parameters
        appropriate to the container layout type

        :param args: miscelaneous positional parameters passed on to self._container_layout.addLayout()
        :type args: tuple
        :param args: miscelaneous keyword parameters passed on to self._container_layout.addLayout()
        :type args: tuple
        :return: n/a
        :rtype: n/a
        """
        self._container_layout.addLayout(*args, **kwargs)

    # --------------------------------------------------------------------------
    # ui definition
    # --------------------------------------------------------------------------
    def _build_ui(self):
        """
        Defines all ui elements

        :return: n/a
        :rtype: n/a
        """
        # header
        self._header_label = QCollapsableLabel(self._header_title, height=self._header_height, parent=self)

        # collapsable widget
        self._container_frame = QtWidgets.QFrame(parent=self)
        self._container_frame.setObjectName("container")
        self._container_frame.setLayout(self._container_layout)

        # main layout
        self._main_layout = QtWidgets.QVBoxLayout()
        self._main_layout.setSpacing(0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._header_label, 0, QtCore.Qt.AlignTop)
        self.setLayout(self._main_layout)

    # --------------------------------------------------------------------------
    # ui initialization
    # --------------------------------------------------------------------------
    def _initialize_ui(self):
        """
        Initializes all ui elements to their default state

        :return: n/a
        :rtype: n/a
        """
        self.set_expanded(self._header_label.is_expanded)

    # --------------------------------------------------------------------------
    # SIGNALS/SLOTS
    # --------------------------------------------------------------------------
    def set_expanded(self, state):
        """
        Sets the main frame widget's expanded/collapsed state
        and rezsizes the overall widget to fit to contents

        :param state: the expanded state
        :type state: bool
        :return: n/a
        :rtype: n/a
        """
        if state:
            self._container_frame.setHidden(False)
            self._container_frame.setParent(self)
            self._main_layout.addWidget(self._container_frame, 1)

        else:
            self._container_frame.setHidden(True)
            self._container_frame.setParent(None)
            self._main_layout.removeWidget(self._container_frame)

        self._container_frame.adjustSize()
        self.adjustSize()

        self.toggled.emit(state)
        self._header_label.set_expanded(state)

    def _connect_signals(self):
        """
        Defines all SIGNAL/SLOT connections

        :return: n/a
        :rtype: n/a
        """
        # connect signals/slots
        self._header_label.toggled.connect(self.set_expanded)

    def resizeEvent(self, event):
        """
        Extended resize event to emit the current size of this widget

        :param event: the resize event beiong handled
        :type event: instance of QResizeEvent
        :return: n/a
        :rtype: n/a
        """
        self.resized.emit(event.size())
        super(QCollapsableFrame, self).resizeEvent(event)


class QClickableLabel(QtWidgets.QLabel):
    """
    Simple clickable label object

    Custom SIGNALS:
        clicked: emitted on mouse release
        toggled: emits a boolean value on mouse release

    Public Attributes:
        :attr is_checked: the checked state of this widget
        :typr is_checked: bool
        :attr set_checked: sets the checked state of this widget
        :type set_checked: method
    """
    clicked = QtCore.pyqtSignal()
    toggled = QtCore.pyqtSignal(bool)

    def __init__(self, text='', parent=None):
        """
        Defines and initializes each instance object

        :param text: label text
        :type text: string
        :param parent: this widgets parent
        :type parent: instance of <class 'QObject'>
        :return: n/a
        :rtype: n/a
        """
        super(QClickableLabel, self).__init__(text, parent)
        self._checked = True

    @property
    def is_checked(self):
        """
        Returns the checked state of this widget

        :return: the checked state of this widget
        :rtype: bool
        """
        return self._checked

    def set_checked(self, state):
        """
        Sets the checked state of this widget

        :param state: the check state
        :type state: bool
        :return: n/a
        :rtype: n/a
        """
        # toggle !
        self._checked = state
        self.toggled.emit(self._checked)

    # --------------------------------------------------------------------------
    # class overrides
    # --------------------------------------------------------------------------
    def mouseReleaseEvent(self, QMouseEvent):
        """
        Handles mouse release events

        :param QMouseEvent: the mouse event being handled
        :type QMouseEvent: instance of <class 'QMouseEvent'>
        :return: n/a
        :rtype: n/a
        """
        # click !
        self.clicked.emit()

        # toggle !
        self._checked = not(self._checked)
        self.toggled.emit(self._checked)
