#!/usr/bin/env python
import rospy
import sys
import json
import yaml
import websocket
from threading import *
from rospy_message_converter import message_converter
from monitor.msg import *
from std_msgs.msg import *

ws_lock = Lock()

def callbackdetectRed(data):
	global ws, ws_lock
	rospy.loginfo('monitor has observed: ' + str(data))
	dict = message_converter.convert_ros_message_to_dictionary(data)
	dict['topic'] = 'detectRed'
	dict['time'] = rospy.get_time()
	ws_lock.acquire()
	logging(dict)
	ws_lock.release()
	rospy.loginfo('event has been successfully logged')
pub_dict = {}
msg_dict = { 'detectRed' : "std_msgs/Int16"}
def monitor():
	global pub_error, pub_verdict
	with open(log, 'w') as log_file:
		log_file.write('')
	rospy.init_node('offline_monitor_FUAV', anonymous=True)
	pub_error = rospy.Publisher(name = 'offline_monitor_FUAV/monitor_error', data_class = MonitorError, latch = True, queue_size = 1000)
	pub_verdict = rospy.Publisher(name = 'offline_monitor_FUAV/monitor_verdict', data_class = String, latch = True, queue_size = 1000)
	rospy.Subscriber('detectRed', Int16, callbackdetectRed)
	rospy.loginfo('monitor started and ready')

def logging(json_dict):
	try:
		with open(log, 'a+') as log_file:
			log_file.write(json.dumps(json_dict) + '\n')
		rospy.loginfo('event logged')
	except:
		rospy.loginfo('Unable to log the event.')

def main(argv):
	global log, actions, ws
	log = './log_FUAV.txt' 
	actions = {
		'detectRed' : ('log', 1)
	}
	monitor()
	rospy.spin()

if __name__ == '__main__':
	main(sys.argv)
