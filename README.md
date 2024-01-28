# ROS Monitor for an FUAV
This repository consists of offline and online monitors for the FUAV [here](https://github.com/iagosilvestre/tello_ros.git).

1. Download the monitor folder and place it in ```~/<your_catkin_ws>/src```. 
2. Make the monitor codes executable:
   ```
   chmod +x ~/<your_catkin_ws>/src/monitor/src/offline_monitor_FUAV.py
   chmod +x ~/<your_catkin_ws>/src/monitor/src/online_monitor_FUAV.py
   ```
3. use ```colcon``` command to build. 

## Offline Monitoring
Here we run the ROS nodes first and let the offline monitor log the events. Once the execution is finished, we can use the offline oracle to verify the logged events.


