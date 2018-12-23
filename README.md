# Bringdrink_robot
Robotics Project Instructions

Extract the folders in the zip.
ROS Kinetic and catkin must be installed. After moving the bring_drink folder into catkin_ws folder:

- cd catkin_ws
- catkin_make

commands must be executed. Then;

To export environment models:

- export GAZEBO_MODEL_PATH= /path-to-models-folder/

To install required packages:
- python -m pip install --upgrade pip setuptools wheel
- pip install pocketsphinx
- pip install pyaudio

To make the source codes executable:

- chmod +x <path-to-defineGoal.py>
- chmod +x <path-to-voice_control_kws.py>
- chmod +x <path-to-object_detector.py>

To prepare the environment (*these commands must be executed for each terminal):

- source /opt/ros/kinetic/setup.bash
- source ~/catkin_ws/devel/setup.bash

To run project : 

- roslaunch bring_drink bring_drink.launch

Another terminal must be opened for speech recognition code *

- cd catkin_ws/bring_drink/src
- rosrun bring_drink voice_control_kws.py

Another terminal must be opened for object detection code *

- cd catkin_ws
- rosrun bring_drink object_detector.py

Another terminal must be opened for moving the robot *

- cd catkin_ws
- rosrun bring_drink defineGoal.py

Now, robot is ready to take and serve orders.
Also for giving orders, a mic is needed.
