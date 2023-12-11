import numpy as np
import pylab as pl
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from sys import platform as _platform


class SimpleEnvironment(object):
    """
    Robots are assumed to be points. Obstacles are assumed to be axis-aligned
    rectangles, inflated by robot radius.
    """

    def __init__(self, map_id=1):
        self.lower_limits = np.array([-0.30, -0.30])
        self.upper_limits = np.array([0.30, 0.60])

        self.robots = []
        self.robot_radius = 0.05
        self.inflation_radius = 0.01

        self.map_id = map_id
        self.InitMap()

    def ComputeDistance(self, config1, config2):
        """Computes Euclidean distance between two points in environment"""
        dist = np.linalg.norm(config1-config2)
        return dist

    def SampleConfig(self):
        """Generates random configuration in free configuration space."""
        while True:
            rand_config = self.lower_limits + np.multiply(np.random.rand(1,2),self.upper_limits-self.lower_limits)[0]
            if (not (self.CheckCollision(rand_config))):
                return rand_config

    def CheckCollision(self, config):
        """Checks for collision between robot at config and obstacles in env
        Currently implements a naive check, assumed to be axis-aligned and
        defined in specific format: [bottom left, __, top right, __].
        """
        # TODO implement better method with FCL
        for o in self.obstacles:
            bl = o[0]
            tr = o[2]
            if(config[0] > bl[0] and config[0] < tr[0]):
                if(config[1] > bl[1] and config[1] < tr[1]):
                    return True
        return False

    def CheckCollisionMultiple(self, composite_config):
        """Check for robot-robot and robot-environment collisions.
        Input: composite configuration (numpy array of configurations)
        """
        # TODO make this collision checking much better
        n_robots = len(composite_config)

        for i in range(n_robots):
            # Check robot-environment collision
            collision_r_e = self.CheckCollision(composite_config[i])
            if collision_r_e:
                return True

            # Check robot-robot collision
            for j in range(i+1, n_robots):
                # if (i == j):
                #     continue
                dist = self.ComputeDistance(composite_config[i], composite_config[j])
                if (dist < self.robot_radius+0.0005):  # TODO move this hard-coded cushion
                    return True
        return False

    def CollisionOnLine(self, config1, config2):
        """Checks for collision on line between two points in env.
        Checks at n points along line.
        """
        # check end points
        if self.CheckCollision(config1):
            return True

        if self.CheckCollision(config2):
            return True

        # setup checker function
        dy = config2[1]-config1[1]
        dx = config1[0]-config2[0]
        b = config2[0]*config1[1]-config1[0]*config2[1]

        f = lambda x: (dy*x[0] + dx*x[1] + b)

        for o in self.obstacles:
            # if line segment is on one side of the box, skip
            bl = o[0]
            tr = o[2]
            if(config1[0]>tr[0] and config2[0]>tr[0]):
                continue
            if(config1[0]<bl[0] and config2[0]<bl[0]):
                continue
            if(config1[1]>tr[1] and config2[1]>tr[1]):
                continue
            if(config1[1]<bl[1] and config2[1]<bl[1]):
                continue
            # otherwise check four corner are on the same side of the line
            result = np.array(map(f, o))

            if (not np.all(result>0)) and (not np.all(result<0)):
                return True
                # return True

        return False

    ############## Plotting stuff #################
    def InitMap(self):
        """Add all obstacles in env.
        Obstacles are currently defined here as polygons.
        [bottom left, bottom right, top right, top left]
        """
        self.obstacles = []

        if self.map_id == 1:        # OPEN MAP
            pass

        if self.map_id == 2:        # I-MAP
            box1 = np.array([[-0.30, -0.30], [0.30, -0.30], [0.30, -0.10], [-0.30, -0.10]])
            box2 = np.array([[-0.30, 0], [-0.05, 0], [-0.05, 0.30], [-0.30, 0.30]])
            box3 = np.array([[0.05, 0], [0.30, 0], [0.30, 0.30], [0.05, 0.30]])
            box4 = np.array([[-0.3, 0.4], [0.30, 0.4], [0.30, 0.60], [-0.3, 0.60]])
            self.obs_unexpanded = [box1, box2, box3, box4]

            self.obstacles.append(box1)
            self.obstacles.append(box2)
            self.obstacles.append(box3)
            self.obstacles.append(box4)
