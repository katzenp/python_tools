"""
arithmetic.py

Description:
    Facilities and objects for performing mathematical  algebra computations
"""
# stdlib
import math


# =============================================================================
# computations - general
# =============================================================================
def isEqual(valueA, valueB, epsilon=0.00001):
    """
    Compares 2 float values to see if they are equal within the 
    given percentage passed to the `epsilon` parameter 

    :param valueA : the first value
    :type valueA : float
    :param valueB : the second value
    :type valueB : float
    :param epsilon: how close the 2 numbers need to be to be considered equal
    :type epsilon : float
    :return: comparison result as a boolean
    :rtype: bool
    """
    minValue = math.fabs(valueA) - (math.fabs(valueA) * epsilon)
    maxValue = math.fabs(valueA) + (math.fabs(valueA) * epsilon)
    print("%s --> %s <-- %s" % (min, math.fabs(valueB), max))
    if math.fabs(valueB) > minValue and math.fabs(valueB) < maxValue:
        return True
    else:
        return False


def iterDivideDistance(posA, posB, divisions=2):
    """
    Divides the distance from posA to posB into equal divisions and
    generates the start and end points for each segment  

    :param posA: start position
    :type posA: list
    :param posB: end position
    :type posB: list
    :param divisions: number of divisions
    :type divisions: int
    :return: new positions
    :rtype: generator object
    """
    if divisions > 1:
        distBetween = [b - a for a, b in zip(posA, posB)]
        for i in xrange(1, divisions):
            factor = i / float(divisions)
            newPos = [(posA[i] + (distBetween[i] * factor)) for i in xrange(3)]
            yield newPos
    else:
        for pos in [posA, posB]:
            yield pos


def getPositions(posA, posB, numDivisions=2):
    """
    Divides the distance from posA to posB into equal divisions and
    returns a list of the start and end points for each segment  

    :param posA: start position
    :type posA: list
    :param posB: end position
    :type posB: list
    :param divisions: number of divisions
    :type divisions: int
    :return: new positions
    :rtype: generator object
    """
    positions = [posA, posB]
    for division in iterDivideDistance(posA, posB, numDivisions):
        if division not in positions:
            positions.insert(-1, division)
    return positions


def getSquareGrid(number):
    """
    Returns the most square grid dimensions from the given number

    :param number: Number of items you want in the grid
    :type number: int
    :return: the width, height, and remainder
    :rtype: list
    """
    height = int(math.sqrt(number))
    width, remainder = divmod(number, height)
    rval = sorted([width, height])
    rval.append(remainder)
    return rval


def getBestGrid(number):
    """
    Returns grid dimensions containing the least empty cells from the given number

    :param number: Number of items you want in the grid
    :type number: int
    :return: the width, height, and remainder
    :rtype: list
    """
    distance = number
    size = None
    for i in range(number / 2):
        i += 1
        j, k = divmod(number, i)
        dif = abs(i - j) + abs(j - k)
        if dif < distance:
            distance = dif
            size = (i, j, k)
    rval = sorted(size[:2])
    rval.append(k)
    return rval


# ==============================================================================
# computations - trig
# ==============================================================================
def degreesToRadians(degrees):
    """
    Converts the given degrees angle to a radian angle

    :param degrees: angle you wish to convert
    :type degrees: float
    :return: angle in radians
    :rtype: float
    """
    return degrees * (math.pi / 180.00)


def radiansToDegrees(radians):
    """
    Converts the given radian angle to a degree angle

    :param radians: angle you wish to convert
    :type radians: float
    :return: angle in degrees
    :rtype: float
    """
    return radians * (180.00 / math.pi)


# ==============================================================================
# vectors
# ==============================================================================
class NVector(tuple):
    """ Tuple representing an nDimensional Vector """
    def __init__(self, *args):
        if not args:
            raise ValueError('Illegal Vector size: 0D')
        super(Vector, self).__init__(*args)

    # --------------------------------------------------------------------------
    # general
    # --------------------------------------------------------------------------
    def magnitude(self):
        """ Returns the magnitude of this vector """
        mag = 0.0
        for each in self:
            mag += math.pow(each, 2)
        return math.sqrt(mag)

    def invert(self):
        """ Returns the additive inverse of this vector """
        inv = (each * -1 for each in self)
        return Vector(inv)

    def unitize(self):
        """ Returns the unit vector for this vector """
        mag = self.magnitude()
        if mag == 0:
            raise ZeroDivisionError("Illegal operation: Division by zero")
        return Vector(each / mag for each in self)

    def dot(self, other):
        """
        Returns the dot product of this vector and another

        :param other: {tuple, list, instance of <class'Vector'>}
            The right hand operand for the dot product formula
        :return: float
        """
        dot = 0.0
        for a, b in zip(self, other):
            dot += (a * b)
        return dot

    def cross(self, other):
        """
        Returns the cross product of this vector and another

        :param other: {tuple, list, Vector}
            The right hand operand for the cross product formula
        :return:
        """
        if len(self) != 3 or len(other) != 3:
            raise ValueError("Cross product requires two 3D Vectors")
        x = (self[1] * other[2]) - (self[2] * other[1])
        y = (self[2] * other[0]) - (self[0] * other[2])
        z = (self[0] * other[1]) - (self[1] * other[0])
        return Vector(x, y, z)

    def distanceTo(self, other):
        """
        Returns the distance from this vector to another

        :param other: :param other: {tuple, list, instance of <class'Vector'>}
            The other vector
        :return: float
        """
        distance = 0.0
        for a, b in zip(self, other):
            a = math.pow(a, 2)
            b = math.pow(b, 2)
            tmp = b - a
            distance += tmp
        distance = abs(distance)
        return math.sqrt(distance)

    def angleBetween(self, other, degrees=False):
        """
        Returns the angle between this vector and another

        :param other: {tuple, list, instance of <class'Vector'>}
            The other vector
        :param degrees: bool
            Option to return the angle in degrees instead of radians
        :return: float
        """
        if not isinstance(other, Vector):
            other = Vector(other)
        unitSelf = self.unitize()
        unitOther = other.unitize()
        radians = math.acos(unitSelf.dot(unitOther))
        if degrees:
            return radians * 57.2958
        return radians

    def rotateBy(self, angle=0.0):
        """
        Returns a new vector representing this vector rotated by the specified
        angle. Angle should be given in degrees

        :param angle: float
            Angle of rotation given in degrees
        :return: instance of <class'Vector'>
        """
        raise NotImplementedError()

    # --------------------------------------------------------------------------
    # operator overrides
    # --------------------------------------------------------------------------
    def __add__(self, other):
        """
        Returns the result of adding the given vector to this one

        :param other: {tuple, list, instance of <class'Vector'>}
            The other vector
        :return: instance of <class'Vector'>
        """
        result = (a + b for a, b in zip(self, other))
        return Vector(result)

    def __radd__(self, other):
        """
        Returns the result of adding this vector to the given vector

        :param other: {tuple, list, instance of <class'Vector'>}
            The other vector
        :return: instance of <class'Vector'>
        """

        result = (a + b for a, b in zip(other, self))
        return Vector(result)

    def __sub__(self, other):
        """
        Returns the result of subtracting the given vector from this one

        :param other: {tuple, list, instance of <class'Vector'>}
            The other vector
        :return: instance of <class'Vector'>
        """
        result = (a - b for a, b in zip(self, other))
        return Vector(result)

    def __rsub__(self, other):
        """
        Returns the result of subtracting this vector from the given vector

        :param other: {tuple, list, instance of <class'Vector'>}
            The other vector
        :return: instance of <class'Vector'>
        """
        result = (a - b for a, b in zip(other, self))
        return Vector(result)

    def __mul__(self, value):
        """
        Returns the result of multiplying this vector by the given value

        :param value: {int, float}
            The scalar to multiply by
        :return: instance of <class'Vector'>
        """
        result = (each * value for each in self)
        return Vector(result)

    def __rmul__(self, value):
        """
        Returns the result of multiplying the given value by this vector

        :param value: {int, float}
            The scalar to multiply by
        :return: instance of <class'Vector'>
        """
        result = (value * each for each in self)
        return Vector(result)

    def __div__(self, value):
        """
        Returns the result of dividing this vector by the given value

        :param value: {int, float}
            The scalar to divide by
        :return: instance of <class'Vector'>
        """
        if value == 0:
            raise ZeroDivisionError("Illegal operation: Division by zero")
        result = (each / value for each in self)
        return Vector(result)


# ==============================================================================
# matrices
# ==============================================================================
class Matrix(list):
    def __init__(self, *rows):
        # error check row ObjectsTestCase
        numColumns = 1
        for r in rows:
            # Rows must be tuples/lists
            if not isinstance(r, (tuple, list)):
                raise TypeError('Rows must be either a list or a tuple')
            # rows must have at least one element
            if not len(r):
                raise ValueError('Row must contain at least one element')
            # rows must have the same number of elements
            if r is rows[0]:
                numColumns = len(r)
                continue
            if len(r) != numColumns:
                raise ValueError('Rows must have the same number of elements')

        # build matrix
        self._data = list(rows)

    # --------------------------------------------------------------------------
    # general
    # --------------------------------------------------------------------------
    @property
    def rowCount(self):
        return len(self._data)

    @property
    def columnCount(self):
        return len(self._data[0])

    @property
    def dimensions(self):
        return (self.rowCount, self.columnCount)

    # --------------------------------------------------------------------------
    # operator overrides
    # --------------------------------------------------------------------------
    def __add__(self):
        pass

    def __radd__(self):
        pass

    def __sub__(self):
        pass

    def __rsub__(self):
        pass

    def __mul__(self):
        pass

    def __rmul__(self):
        pass

    def __div__(self):
        pass

    def __rdiv__(self):
        pass
