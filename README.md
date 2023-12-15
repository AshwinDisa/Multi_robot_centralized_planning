# Multi_robot_centralized_planning

### Tested with 

Python 2.7.18, Python 3.10.12

### Dependencies

Numpy, cPickle, Pygame

### Clone the repository in your desired workplace
```
git clone https://github.com/AshwinDisa/Multi_robot_centralized_planning.git
```
To run the package
```
cd ~/python/
python2 run.py
```
In run.py file, there are 2 cases 

1) map_id = 1 and test = 3 for 5 robots in open map (circular formation)

2) map_id = 2 and test = 2 for 4 robots in I map

To visualize the results
```
cd ~/visualization/
python3 4_robot_H_ shape.py # for case 1
python3 5_robot_circle.py # for case 2
```

To recreate the results copy the resulting path dictionary from the output of run.py and paste in the ~/visualization/scaling.py file to scale the coordinates for plotting,


Copy Paste the resulting output into one of the python3 visualization files listed earlier and run the script.

## Visualizations using Pygame

https://github.com/AshwinDisa/Multi_robot_centralized_planning/assets/69672043/a4adaec2-d270-4d85-8d38-e30e69af26d5

https://github.com/AshwinDisa/Multi_robot_centralized_planning/assets/69672043/c066973b-7512-4901-b0df-42a1b92e0982



