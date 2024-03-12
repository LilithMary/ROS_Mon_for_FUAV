# ROS Monitor for an FUAV
This repository consists of offline and online monitors for the FUAV [here](https://github.com/iagosilvestre/tello_ros.git).

<!-- At this stage the aim is to observe and log the messages of particular topics. No properties have yet been provided for the oracles to check. Therefore, as a first step, the monitors only track messages published on topic ```detectRed``` of type ```std_msgs.msg.Int16``` by node ```example_node``` in package ```my_ros_package```. -->

## Topics to Monitor
We are interested in observing the below topics:

```
/agLand [std_msgs/msg/String]
/agentReact [std_msgs/msg/String]
/battery [std_msgs/msg/Int16]
/cmd_vel [geometry_msgs/msg/Twist]
/detectRed [std_msgs/msg/Int16]
```
## Properties

1. If the drone detects a red light within 100 and 101 time steps ago, then it should publish a message 'reactRed' on topic 'agentReact'.
    
```
detectRedPredicate is 'True' if and only if detectRed > 200.
(once[100:101]({topic: 'detectRed', detectRedPredicate: 'True'}) -> {topic: 'agentReact', data: 'reactRed'} )
```

2. If the remaining battery percentage is between 20 and 40 inclusive, then the drone should publish a message 'safetyLanding' on topic 'agLand'.
```
batteryPredicate is 'Safety' if and only if battery >= 20 and battery <= 40.
({topic: 'battery', batteryPredicate: 'Safety'} -> {topic: 'agLand', data: 'safetyLanding'})
```

3. If the remaining battery percentage is strictly less than 20, then the drone should publish a message 'criticalLanding' on topic 'agLand'.
```
batteryPredicate is 'Critical' if and only if batter < 20.
({topic: 'battery', batteryPredicate: 'Critical'} -> {topic: 'agLand', data: 'criticalLanding'})
```

4. The drone should never more backwards, i.e. its velocity in the y axis should be always non-negative.
```
(forall[t]. {topic: 'cmd_vel', time: *t} -> {topic: 'cmd_vel', forwardMotion: 'True', time: *t})
```

## Instructions
After downloading the main repository, take the following steps to integrate the monitors:

1. Download the ```monitor``` and ```rosmonitoring_interfaces``` folders and place them in ```~/<your_colcon_ws>/src```. 
2. Make the monitor codes executable:
   ```
   chmod +x ~/<your_colcon_ws>/src/monitor/src/offline_monitor_FUAV.py
   chmod +x ~/<your_colcon_ws>/src/monitor/src/online_monitor_FUAV.py
   ```
3. use ```colcon``` command to build. 

### Offline Monitoring
Here we run the ROS nodes first and let the offline monitor log the events. Once the execution is finished, we can use the offline oracle to verify the logged events.

#### Run ROS monitoring node
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash
source /install/local_setup.bash
source /install/setup.bash

ros2 launch monitor offline_monitor_launch.py
```

#### Run gazebo simulation
As instructed in [here](https://github.com/iagosilvestre/tello_ros?tab=readme-ov-file#run-simulation).

Interrupt the runs in each terminal to end the processes. 
All events observed by the ROS monitor should be in ```~/<your_colcon_ws>/log_FUAV_offline.txt```.

#### Run Oracle on logged events
```
cd <your_ROSMonitoring_path>/oracle/TLOracle/
./oracle.py --offline --property tello_ros_mon_temporal_properties --trace <your_log_file.txt> --discrete
```
Note that the property file is a Python file but the extension (.py) must be omitted in the oracle command above. 

### Online Monitoring:
Here we run the online oracle before running the ROS nodes so that the verdicts are published as the nodes are active.

#### Run Oracle
```
cd <your_ROSMonitoring_path>/oracle/TLOracle/
python3 oracle.py --discrete --online --property dummy
```

#### Run ROS monitoring node
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash
source /install/local_setup.bash
source /install/setup.bash

ros2 launch monitor online_monitor_launch.py
```

