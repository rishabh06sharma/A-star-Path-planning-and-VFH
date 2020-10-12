# A-star-Path-planning-and-VFH

Autonomously plan and execute a path for a robot in the Stage simulator from a start location to a goal location, given a map. The global plan is given by A* and the local planning is done using a modified Vector Field Histogram (VFH) in the 2D plane. <br />

![](https://github.com/rs278/A-star-Path-planning-and-VFH/blob/master/docs/a_star.gif)

#### Steps to follow:
1. Create package inside /catkin_ws/src/
```python
catkin_create_pkg ros_pa2 std_msgs geometry_msgs rospy roscpp
```
2. Copy files inside package and follow:
```python
cd ~/catkin_ws
catkin_make
source ~/.bashrc
```
3. Grant execution permission to the script or .py file
```python
chmod +x <.py file directory>
```
4. Run program by roslaunch:
```python
roslaunch ros_pa2 pa2.launch
```

#### Global Planner/Optimal path finder (A*): <br />
Total Cost <br />
f(n) = g(n) + ε.h(n) <br />
where g(n) exact cost of path from start node to node h(n)​ is the heuristic function which estimates a cost from node n to the goal node. ε is tuning perameter.
<br />
#### Local Planner/obstacle avoidance (VFH): <br />
G = a * target_direction  + b * current_direction  + c * previous_direction
a,b,c are the tuning perameters
