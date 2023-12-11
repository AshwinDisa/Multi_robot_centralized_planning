from simple_environment import SimpleEnvironment
from prm_graph import Graph
import cPickle as pickle
import numpy as np
import time
import sys


class PRMPlanner(object):
    """PRM planner node: interfaces with environment and graph structure.
    Can either generate a new roadmap or load a saved one.
    """

    def __init__(self, map_id=1, filepath=None):
        self.env = SimpleEnvironment(map_id)
        self.graph = Graph(self.env)
        self.map_id = map_id

        if map_id == 1 and filepath is None:
            filepath = '../roadmaps/cube_center.p'
        elif map_id == 2 and filepath is None:
            filepath = '../roadmaps/t_map_simple.p'

        self.LoadRoadmap(filepath)

    def LoadRoadmap(self, filepath):
        """Loads pickle with pre-made roadmap."""
        print("Loading roadmap.")
        with open(filepath, 'rb') as f:
            prm_graph = pickle.load(f)
            self.graph.vertices = prm_graph['vertices']
            self.graph.edges = prm_graph['edges']
            print self.graph.vertices
            print self.graph.edges


    def FindPath(self, sconfig, gconfig):
        """Find nearest vertices to sconfig and gconfig
        raw_input should be in numpy arrays of dim 3 (x,y,theta)
        """
        sid = self.graph.GetNearestNode(sconfig[0:2])
        gid = self.graph.GetNearestNode(gconfig[0:2])
        start_angle = sconfig[2]
        goal_angle = gconfig[2]

        point_path = self.graph.Djikstra(sid, gid)
        if len(point_path) == 0:
            return []

        # Add angles and sconfig, gconfig
        path = self.PostProcessPRMPath(point_path, sconfig, gconfig)

        if self.visualize:
            self.VisualizePath(point_path)
        return path
