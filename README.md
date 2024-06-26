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

1. If the drone publishes a message 'reactRed' on topic 'agentReact', it must have detected a red light within 100 and 101 time steps ago.
    
```
detectRedPredicate is 'True' if and only if detectRed > 200.
({topic: 'agentReact', data: 'reactRed'} -> once[100:101]{topic: 'detectRed', detectRed: 'True'})
```

2. If the drone publishes a message 'safetyLanding' on topic 'agLand', then the remaining battery percentage must have been between 20 and 40 inclusive within 100 and 101 time steps ago.
```
batteryPredicate is 'Safety' if and only if battery >= 20 and battery <= 40.
({topic: 'agLand', data: 'safetyLanding'} -> once[100:101]{topic: 'battery', battery: 'Safety'})
```

3. If the drone publishes a message 'criticalLanding' on topic 'agLand', then the remaining battery percentage must have been strictly less than 20 within 100 and 101 time steps ago.
```
batteryPredicate is 'Critical' if and only if battery < 20.
({topic: 'agLand', data: 'criticalLanding'} -> once[100:101]{topic: 'battery', battery: 'Critical'})
```

4. The drone should never move backwards, i.e. its velocity in the y axis should be always non-negative. If the drone publishes a message on topic ```cmd_vel```, then its ```forwardMotion``` must be 'True'.
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

### Online Monitoring with four monitors:
#### Run Oracles in separate terminals on different ports
```
cd <your_ROSMonitoring_path>/oracle/TLOracle/
python3 oracle.py --discrete --online --port 8080 --property tello_ros_mon_temporal_property_1
```
```
cd <your_ROSMonitoring_path>/oracle/TLOracle/
python3 oracle.py --discrete --online --port 8082 --property tello_ros_mon_temporal_property_2
```
```
cd <your_ROSMonitoring_path>/oracle/TLOracle/
python3 oracle.py --discrete --online --port 8083 --property tello_ros_mon_temporal_property_3
```
```
cd <your_ROSMonitoring_path>/oracle/TLOracle/
python3 oracle.py --discrete --online --port 8084 --property tello_ros_mon_temporal_property_4

```

#### Run ROS monitors in separate terminals
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash
source /install/local_setup.bash
source /install/setup.bash

ros2 launch monitor online_monitor_launch_p1.py
```
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash
source /install/local_setup.bash
source /install/setup.bash

ros2 launch monitor online_monitor_launch_p2.py
```
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash
source /install/local_setup.bash
source /install/setup.bash

ros2 launch monitor online_monitor_launch_p3.py
```
```
cd ~/<your_colcon_ws>
source /opt/ros/foxy/setup.bash
source /install/local_setup.bash
source /install/setup.bash

ros2 launch monitor online_monitor_launch_p4.py
```

