"""
Primary algorithm for k-Means clustering

This file contains the Algorithm class for performing k-means clustering.  While it is
the last part of the assignment, it is the heart of the clustering algorithm.  You
need this class to view the complete visualizer.

Jin Ryu jfr224
11/12/2018
"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6checks
import a6dataset
import a6cluster


class Algorithm(object):
    """
    A class to manage and run the k-means algorithm.

    INSTANCE ATTRIBUTES:
        _dataset [Dataset]: the dataset which this is a clustering of
        _clusters [list of Cluster]: the clusters in this clustering (not empty)
    """


    # Part A
    def __init__(self, dset, k, seeds=None):
        """
        Initializes the algorithm for the dataset ds, using k clusters.

        If the optional argument seeds is supplied, it will be a list of indices into the
        dataset that specifies which points should be the initial cluster centroids.
        Otherwise, the clusters are initialized by randomly selecting k different points
        from the database to be the cluster centroids.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter k: the number of clusters
        Precondition: k is an int, 0 < k <= dset.getSize()

        Paramter seeds: the initial cluster indices (OPTIONAL)
        Precondition seeds is None, or a list of k valid indices into dset.
        """
        assert isinstance(dset, a6dataset.Dataset)
        assert type(k) == int and 0 < k and k <= dset.getSize()
        assert seeds == None or a6checks.is_seed_list(seeds, k, dset.getSize())

        self._dataset = dset
        contents = dset.getContents()

        if seeds == None:
            centroids = random.sample(contents, k)
        else:
            centroids = []
            for k in seeds:
                centroids.append(contents[k])

        clusters = []
        for centroid in centroids:
            onecluster = a6cluster.Cluster(dset, centroid)
            clusters.append(onecluster)
        self._clusters = clusters


    def getClusters(self):
        """
        Returns the list of clusters in this object.

        This method returns the attribute _clusters directly.  Any changes made to this
        list will modify the set of clusters.
        """
        return self._clusters


    # Part B
    def _nearest(self, point):
        """
        Returns the cluster nearest to point

        This method uses the distance method of each Cluster to compute the distance
        between point and the cluster centroid. It returns the Cluster that is closest.

        Ties are broken in favor of clusters occurring earlier self._clusters.

        Parameter point: The point to compare.
        Precondition: point is a list of numbers (int or float), with the same dimension
        as the dataset.
        """
        assert a6checks.is_point(point)
        assert len(point) == self._dataset.getDimension()

        distance = float('inf')
        for cluster in self._clusters:
            if distance > cluster.distance(point):
                distance = cluster.distance(point)
        for cluster in self._clusters:
            if distance == cluster.distance(point):
                closest = cluster

        return closest


    def _partition(self):
        """
        Repartitions the dataset so each point is in exactly one Cluster.
        """
        contents = self._dataset.getContents()
        clusters = self._clusters

        for cluster in clusters:
            cluster.clear()

        for point in range(len(contents)):
            closest = self._nearest(contents[point])
            closest.addIndex(point)


    # Part C
    def _update(self):
        """
        Returns true if all centroids are unchanged after an update; False otherwise.

        This method first updates the centroids of all clusters'.  When it is done, it
        checks whether any of them have changed. It then returns the appropriate value.
        """
        unchanged = True
        for cluster in self._clusters:
            after_update = cluster.update()
            if after_update == False:
                unchanged = False
        return unchanged


    def step(self):
        """
        Returns True if the algorithm converges after one step; False otherwise.

        This method performs one cycle of the k-means algorithm. It then checks if
        the algorithm has converged and returns the appropriate value.
        """
        # In a cycle, we partition the points and then update the means.
        self._partition()
        return self._update()


    # Part D
    def run(self, maxstep):
        """
        Continues clustering until either it converges or maxstep steps
        (which ever comes first).

        This method calls step() repeatedly, up to maxstep times, until the
        algorithm converges. It stops after maxstep iterations even if the
        algorithm has not converged.

        Parameter maxstep: the maximum number of steps to try
        Precondition: maxstep is an int >= 0
        """
        assert type(maxstep) == int and maxstep >= 0
        # You do not need a while loop for this.  Just write a for-loop, and exit
        # the for-loop (with a return) if you finish early.
        for step in range(maxstep):
            self.step()
            if self.step() == True:
                return "done after the algorithm convered"
        return "done after the maximum number of steps to try"
