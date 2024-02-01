# ROS Monitor for an FUAV
This repository consists of offline and online monitors for the FUAV [here](https://github.com/iagosilvestre/tello_ros.git).

At this stage the aim is to observe and log the messages of particular topics. No properties have yet been provided for the oracles to check. Therefore, as a first step, the monitors only track messages published on topic ```detectRed``` of type ```std_msgs.msg.Int16``` by node ```example_node``` in package ```my_ros_package```. 

After downloading the main repository, take the following steps to integrate the monitors:

1. Download the ```monitor``` and ```rosmonitoring_interfaces``` folders and place them in ```~/<your_colcon_ws>/src```. 
2. Make the monitor codes executable:
   ```
   chmod +x ~/<your_colcon_ws>/src/monitor/src/offline_monitor_FUAV.py
   chmod +x ~/<your_colcon_ws>/src/monitor/src/online_monitor_FUAV.py
   ```
3. use ```colcon``` command to build. 

## Offline Monitoring
Here we run the ROS nodes first and let the offline monitor log the events. Once the execution is finished, we can use the offline oracle to verify the logged events.

### Run ROS monitoring node
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash

ros2 launch monitor run_offline_monitor.launch
```

### Run gazebo simulation
As instructed in [here](https://github.com/iagosilvestre/tello_ros?tab=readme-ov-file#run-simulation).

Interrupt the runs in each terminal to end the processes. 
All events observed by the ROS monitor should be in ```~/<your_colcon_ws>/offline_FUAV_log.txt```.

### Run Oracle on logged events
[To Do]

## Online Monitoring:
Here we run the online oracle before running the ROS nodes so that the verdicts are published as the nodes are active.

[To Do]
