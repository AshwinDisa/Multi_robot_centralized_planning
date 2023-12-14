#!/usr/bin/env python

import numpy as np
import cPickle as pickle
from simple_environment import SimpleEnvironment
from prm_planner import PRMPlanner
from mrdrrt_planner import MRdRRTPlanner

def main():

    # Two test cases
    # 1) map_id = 1 and test = 3 for 5 robots in open map (circular formation)
    # 2) map_id = 2 and test = 2 for 4 robots in I map

    prm = PRMPlanner(map_id=1, filepath=None)

    test = 3

    if test == 1:
        # Test 1 robot
        sconfigs = np.array([[0, 0.3], [-0.4, -0.3]])
        gconfigs = np.array([[0.4, -0.3], [0, 0.2]])

    if test == 2:

        # Test 4 robots - Works
        sconfigs = np.array([[-0.25, -0.05], [0.25, -0.05], [-0.25, 0.35], [0.25, 0.35]])
        gconfigs = np.array([[0.30, -0.05], [-0.3, -0.05], [0.30, 0.35], [-0.3, 0.35]])

    if test == 3:

        # Test 5 robots - Works
        sconfigs = np.array([[0.3, 0.0], [0.09, 0.28], [-0.24, 0.17], [-0.24, -0.17], [0.09, -0.28]])
        gconfigs = np.array([[-0.3, 0.0], [-0.09, -0.28], [0.24, -0.17], [0.24, 0.17], [-0.09, 0.28]])

    if test == 4:

        # 6 robots
        sconfigs = np.array([[0.13, 0.22], [-0.12, 0.22], [-0.25, 0.0], [-0.13, -0.22], [0.13, -0.22], [0.25, -0.0]])
        gconfigs = np.array([[-0.13, -0.22], [0.13, -0.22], [0.25, -0.0], [0.13, 0.22], [-0.12, 0.22], [-0.25, 0.0]])

    if test == 5:

        # 8 robots
        sconfigs = np.array([[0.18, 0.18], [0.0, 0.25], [-0.18, 0.18], [-0.25, 0.0], [-0.18, -0.18], [-0.0, -0.25], [0.18, -0.18], [0.25, -0.0]])
        gconfigs = np.array([[-0.18, -0.18], [-0.0, -0.25], [0.18, -0.18], [0.25, -0.0], [0.18, 0.18], [0.0, 0.25], [-0.18, 0.18], [-0.25, 0.0]])

    if test == 6:

        sconfigs = np.array([[-0.25, -0.05], [0.25, -0.05], [0, 0.25]])
        gconfigs = np.array([[0.30, -0.05], [0, 0.30], [-0.30, -0.05]])

    mrdrrt = MRdRRTPlanner(prm, n_robots=sconfigs.shape[0], visualize=True)
    path = mrdrrt.FindPath(sconfigs, gconfigs)
    print(path)


if __name__ == "__main__":
    main()

