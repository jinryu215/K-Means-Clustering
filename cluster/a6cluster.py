"""
Cluster class for k-Means clustering

This file contains the class cluster, which is the second part of the assignment.  With
this class done, the visualization can display the centroid of a single cluster.

Jin Ryu jfr224
11/10/2018
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6checks
import a6dataset


class Cluster(object):
    """
    A class representing a cluster, a subset of the points in a dataset.

    A cluster is represented as a list of integers that give the indices in the dataset
    of the points contained in the cluster.  For instance, a cluster consisting of the
    points with indices 0, 4, and 5 in the dataset's data array would be represented by
    the index list [0,4,5].

    A cluster instance also contains a centroid that is used as part of the k-means
    algorithm.  This centroid is an n-D point (where n is the dimension of the dataset),
    represented as a list of n numbers, not as an index into the dataset. (This is because
    the centroid is generally not a point in the dataset, but rather is usually in between
    the data points.)

    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset this cluster is a subset of
        _indices [list of int]: the indices of this cluster's points in the dataset
        _centroid [list of numbers]: the centroid of this cluster
    EXTRA INVARIANTS:
        len(_centroid) == _dataset.getDimension()
        0 <= _indices[i] < _dataset.getSize(), for all 0 <= i < len(_indices)
    """


    # Part A
    def __init__(self, dset, centroid):
        """
        Initializes a new empty cluster whose centroid is a copy of <centroid>

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter centroid: the cluster centroid
        Precondition: centroid is a list of dset.getDimension() numbers
        """
        assert isinstance(dset, a6dataset.Dataset)
        assert a6checks.is_point(centroid) and len(centroid) == dset.getDimension()

        self._dataset = dset
        self._indices = []
        m = []
        for x in range(len(centroid)):
            m.append(centroid[x])
        self._centroid = m


    def getCentroid(self):
        """
        Returns the centroid of this cluster.

        This getter method is to protect access to the centroid.
        """
        return self._centroid


    def getIndices(self):
        """
        Returns the indices of points in this cluster

        This method returns the attribute _indices directly.  Any changes made to this
        list will modify the cluster.
        """
        return self._indices


    def addIndex(self, index):
        """
        Adds the given dataset index to this cluster.

        If the index is already in this cluster, this method leaves the
        cluster unchanged.

        Precondition: index is a valid index into this cluster's dataset.
        That is, index is an int in the range 0.._dataset.getSize()-1.
        """
        assert type(index) == int
        assert 0 <= index and index <= self._dataset.getSize()-1

        points = self.getIndices()
        if not index in points:
            points.append(index)


    def clear(self):
        """
        Removes all points from this cluster, but leave the centroid unchanged.
        """
        self._indices = []


    def getContents(self):
        """
        Returns a new list containing copies of the points in this cluster.

        The result is a list of list of numbers.  It has to be computed from the indices.
        """
        copy = []
        indices = self._indices
        dataset = self._dataset
        all_contents = dataset.getContents()
        for x in range(len(indices)):
            newpoint = all_contents[indices[x]]
            copy.append(newpoint)

        return copy


    # Part B
    def distance(self, point):
        """
        Returns the euclidean distance from point to this cluster's centroid.

        Parameter point: The point to be measured
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the centroid.
        """
        assert a6checks.is_point(point)
        assert len(point) == len(self._centroid)

        centroid = self._centroid
        dist_squared = 0
        for dim in range(len(point)):
            oneD_distance = centroid[dim] - point[dim]
            dist_squared += oneD_distance * oneD_distance
        distance = math.sqrt(dist_squared)

        return distance


    def getRadius(self):
        """
        Returns the maximum distance from any point in this cluster, to the centroid.

        This method loops over the contents to find the maximum distance from
        the centroid.  If there are no points in this cluster, it returns 0.
        """
        if self._indices == []:
            return 0
        dataset = self._dataset
        indices = self._indices
        centroid = self._centroid
        distance = 0
        for x in range(len(indices)):
            point = dataset.getPoint(indices[x])
            if distance <= self.distance(point):
                distance = self.distance(point)
        return distance


    def update(self):
        """
        Returns True if the centroid remains the same after recomputation; False otherwise.

        This method recomputes the _centroid attribute of this cluster. The new _centroid
        attribute is the average of the points of _contents (To average a point, average
        each coordinate separately).

        Whether the centroid "remained the same" after recomputation is determined by
        numpy.allclose.  The return value should be interpreted as an indication of whether
        the starting centroid was a "stable" position or not.

        If there are no points in the cluster, the centroid. does not change.
        """
        dataset = self._dataset
        indices = self._indices
        oldcentroid = []
        for x in range(len(self._centroid)):
            oldcentroid.append(self._centroid[x])
        dim = dataset.getDimension()

        points = []
        for th in range(len(indices)):
            point = dataset.getPoint(indices[th])
            points.append(point)

        new_centroid = []
        for x in range(dim):
            sum = 0
            for th in range(len(points)):
                sum += points[th][x]
            mean = sum / len(points)
            new_centroid.append(mean)

        self._centroid = new_centroid
        return numpy.allclose(oldcentroid, new_centroid)


    # PROVIDED METHODS: Do not modify!
    def __str__(self):
        """
        Returns a String representation of the centroid of this cluster.
        """
        return str(self._centroid)

    def __repr__(self):
        """
        Returns an unambiguous representation of this cluster.
        """
        return str(self.__class__) + str(self)
