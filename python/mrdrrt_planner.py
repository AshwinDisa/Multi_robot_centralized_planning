import numpy as np
import pylab as pl
import time

from prm_graph import Graph
from simple_environment import SimpleEnvironment
from prm_planner import PRMPlanner
from mrdrrt_tree import Tree
from implicit_graph import ImplicitGraph

from profile_utils import timefunc
from collections import defaultdict

import cPickle as pickle
import random


class MRdRRTPlanner(object):
    """Multi-robot discrete RRT algorithm for coordinated centralized planning.

    Simple implementation of:

    Solovey, Kiril, Oren Salzman, and Dan Halperin.
    "Finding a needle in an exponential haystack: Discrete RRT for exploration
    of implicit roadmaps in multi-robot motion planning." Algorithmic Foundations
    of Robotics XI. Springer International Publishing, 2015. 591-607.
    """

    def __init__(self, prm, n_robots=2, visualize=False):
        self.n_robots = n_robots
        self.env = prm.env
        self.implicitgraph = ImplicitGraph(self.env, prm, n_robots)
        self.tree = Tree(self.env, self.implicitgraph)
        self.max_iter = 5000
        self.prm = prm  # Here just for VisualizePlot
        self.visualize = visualize

    @timefunc
    def FindClosestToConfig(self, config1, neighbors):
        min_dist = float("inf")
        nearest = None

        for node in neighbors:
            config2 = self.implicitgraph.NodeIdsToConfigs(node)
            dist = self.implicitgraph.ComputeCompositeDistance(config2, config1)
            if(dist < min_dist):
                min_dist = dist
                nearest = node

        return min_dist, nearest

    @timefunc
    def Oracle(self, qnear, qrand):
        """Direction oracle, as defined in Oren's paper.
        Given randomly sampled comp config and nearest config on current tree,
        return qnew, a neighbor of qnear on the implicit graph that hasn't been
        explored yet, and is closest (by sum of euclidean distances) to qnear.
        """
        # neighbors = self.implicitgraph.GetNeighbors(qnear)
        #
        # min_dist, nearest = self.FindClosestToConfig(qrand, neighbors)
        nearest = self.implicitgraph.GetClosestCompositeNeighbor(qnear,qrand)
        print "nearest: ", nearest

        # check collision between qnear and nearest node
        # TODO clean this up, move somewhere else
        if nearest:
            nearest_config = self.implicitgraph.NodeIdsToConfigs(nearest)
            qnear_config = self.implicitgraph.NodeIdsToConfigs(qnear)

            for i in range(len(qnear)):
                config1 = qnear_config[i]
                config2 = nearest_config[i]
                if self.env.CollisionOnLine(config1, config2):
                    print "collision"
                    return None

            if not self.LocalConnector(qnear_config, nearest_config):
                print "collision"
                return None

        return nearest

    @timefunc
    def Expand(self, gconfigs):
        """Takes random sample and tries to expand tree in direction of sample.
        """
        if random.random() > 0.3:
            qrand = self.implicitgraph.RandomSample()
        else:
            qrand = gconfigs
        qnear, near_id = self.tree.NearestNeighbors(qrand, 1)
        print "qrand: ", qrand
        print "qnear: ", qnear

        qnew = self.Oracle(qnear, qrand)
        print "qnew: ", qnew

        if (qnew is not None and qnew not in self.tree.vertices):
            new_id = self.tree.AddVertex(qnew)
            self.tree.AddEdge(near_id, new_id)

        print "tree edges: ", self.tree.edges
        print "tree vertices: ", self.tree.vertices
        # raw_input(".")

    @timefunc
    def LocalConnector(self, config1, config2):
        """Check for collision free path between two composite configs.
        Given two composite configurations, check if collision free movement
        between them is possible. If coordinated movement/ordering is required,
        return ordering of robots as list.
        Doing naive implementation first, where robots are moved along path by
        constant phase/alpha from start to end configs and check collision at
        each point.
        Later, do more complicated one.
        Input: lists of node IDs
        """
        n_steps = 10
        steps = [i/float(n_steps) for i in range(n_steps+1)]

        for step in steps:
            q = config1 + (config2-config1)*step
            collision = self.env.CheckCollisionMultiple(q)
            if collision:
                return False  # couldn't connect

        return True  # Connection succeeded!

    @timefunc
    def ConnectToTarget(self, gids):
        """Check if it's possible to get to goal from closest nodes in current tree.
        Called at the end of each iteration.
        Input: list of goal configurations (goal composite config)
        """
        # TODO implement k-nearest neighbors...
        # Actually, how important is this?
        # Only checking closest node right now because that's all nearestneighbors does
        # for q in self.tree.NearestNeighbors(goal,1):

        g_config = self.implicitgraph.NodeIdsToConfigs(gids)
        neighbor, nid = self.tree.NearestNeighbors(g_config, 1)
        n_config = self.implicitgraph.NodeIdsToConfigs(neighbor)
        success = self.LocalConnector(n_config, g_config)
        return success, nid

    def ConstructPath(self, neighbor_of_goal, sconfigs, gconfigs, sids, gids):
        """Returns final path thru implicit graph to get from start to goal.
        Called when a collision-free path to goal config is found.
        Inputs:
            neighbor_of_goal: (node IDs) node that was successfully connected to goal
            gconfigs: list of configurations of final goal
        """
        path = [gconfigs]
        path.append(self.implicitgraph.NodeIdsToConfigs(gids))

        # Follow pointers to parents from goal to reconstruct path, reverse
        node_id = neighbor_of_goal
        while (node_id in self.tree.edges.keys()):  # TODO find better end condition
            node = self.tree.vertices[node_id]
            path.append(self.implicitgraph.NodeIdsToConfigs(node))
            node_id = self.tree.edges[node_id]

        path.append(self.implicitgraph.NodeIdsToConfigs(sids))
        path.append(sconfigs)
        path.reverse()

        return path

    def FindPath(self, sconfigs, gconfigs):
        """Main function for MRdRRT. Expands tree to find path from start to goal.
        Inputs: list of start and goal configs for robots.
        """
        if len(sconfigs) != len(gconfigs):
            print("Start and goal configurations don't match in length")
            return

        raw_input("Wait for start/goal configs, and enter to start planning")

        if self.env.CheckCollisionMultiple(sconfigs) or self.env.CheckCollisionMultiple(gconfigs):
            print("Start or goal configurations are in collision.")
            return

        print("Looking for a path...")
        sids = self.implicitgraph.NearestNodeInGraph(sconfigs)
        gids = self.implicitgraph.NearestNodeInGraph(gconfigs)

        sconfigs2 = self.implicitgraph.NodeIdsToConfigs(sids)
        gconfigs2 = self.implicitgraph.NodeIdsToConfigs(gids)

        # Put start config in tree
        self.tree.AddVertex(sids)

        i = 0
        while (i < self.max_iter):
            self.Expand(gconfigs)
            success, nid = self.ConnectToTarget(gids)
            if success:
                print("Found a path! Constructing final path now..")
                path = self.ConstructPath(nid, sconfigs, gconfigs, sids, gids)
                break

            if(i % 50 == 0):
                print(str(i) + "th iteration")
            i += 1
            # print('-------')

        if (i == self.max_iter):
            print("Failed to find path - hit maximum iterations.")
        else:

            # At this point, path is a list of numpy arrays. Want a dictionary of list of numpy arrays
            path_dict = defaultdict(list)
            for r in range(self.n_robots):
                for t in range(1, len(path)):
                    path_dict[r].append(path[t][r])
            return path_dict
