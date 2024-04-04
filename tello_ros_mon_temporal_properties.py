import oracle

'''
/detectRed [std_msgs/msg/Int16]
/agentReact [std_msgs/msg/String]
/battery [std_msgs/msg/Int16]
/agLand [std_msgs/msg/String]
/cmd_vel [geometry_msgs/msg/Twist]
'''



pl = [
"({topic: 'agentReact', data: 'reactRed'} -> once[100:101]{topic: 'detectRed', detectRed: 'True'})",
"({topic: 'agLand', data: 'safetyLanding'} -> once{topic: 'battery', battery: 'Safety'})",
"({topic: 'agLand', data: 'criticalLanding'} -> once{topic: 'battery', battery: 'Critical'})",
"(forall[t]. {topic: 'cmd_vel', time: *t} -> {topic: 'cmd_vel', forwardMotion: 'True', time: *t})"
]

# property to verify
PROPERTY = ' and '.join(pl)

# predicates used in the property (initialization for time 0)
predicates = dict()

# in here we can add all the predicates we are interested in.. Of course, we also need to define how to translate Json messages to predicates.

# function to abstract a dictionary (obtained from Json message) into a list of predicates
def abstract_message(message):
    print(message)
    predicates = dict()

    predicates['topic'] = message['topic']
    predicates['time'] = str(message['time'])
    
    if message['topic'] in ["agentReact", "agLand", "detectRed", "battery"]:
        predicates['data'] = str(message['data'])
    
    if message['topic'] == "detectRed":
    	detectRed = int(message['data'])
    	predicates['detectRed'] = str((detectRed > 200))
    	
    elif message['topic'] == "battery":
    	percentage = int(message['data'])
    	if percentage >= 20 and percentage <= 40: 
    		predicates['battery'] = 'Safety'
    	elif percentage < 20:
    		predicates['battery'] = 'Critical'
    	else:
    		predicates['battery'] = 'Unspecified'
    		
    elif message['topic'] == 'cmd_vel':
    	linearY = float(message.linear.y)
    	predicates['forwardMotion'] = str((linearY >= 0))
    	
    #print(predicates)
    return predicates
