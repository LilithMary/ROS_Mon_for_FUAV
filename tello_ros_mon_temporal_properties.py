import oracle

# replace "reaction" with field name that carries 'reactRed'
# replace "percentage" with field name that carries 'battery'
# replace "landingMode" with field name that carries 'safetyLanding' and 'criticalLanding'
'''
- /detectRed	std_msgs/Int16		- Amount of red pixels the drone camera is seeing
- /detectBlue	std_msgs/Int16		- Amount of blue pixels the drone camera is seeing
- /battery	std_msgs/Int16		- Battery percentage of the drone
- /cmd_tello	std_msgs/String		- Used to send commands to the tello, for example"move_forward;180"
'''



pl = [
'(once[100:101]({topic: "detectRed", detectRed: True}) -> {topic: "agentReact", reactRed: True} )',
'({topic: "battery", battery: "Safety"} -> {topic: "agLand", landingMode: "Safety"})',
'({topic: "battery", battery: "Critical"} -> {topic: "agLand", landingMode: "Critical"})',
'({topic: "cmd_vel", forwardMotion: True})'
]

# property to verify
PROPERTY = ' and '.join(pl)

# predicates used in the property (initialization for time 0)
predicates = dict()

# in here we can add all the predicates we are interested in.. Of course, we also need to define how to translate Json messages to predicates.

# function to abstract a dictionary (obtained from Json message) into a list of predicates
def abstract_message(message):
    print(message)


    predicates['topic'] = message['topic']

    if message['topic'] == "detectRed":
    	detectRed = int(message['detectRed'])
    	predicates['detectRed'] = (detectRed > 200)
 
    elif message['topic'] == "agentReact":
    	reaction = str(message['agentReact'])
    	predicates['reactRed'] = (reaction == 'reactRed')
    	
    elif message['topic'] == "battery":
    	percentage = int(message['battery'])
    	if percentage >= 20 and percentage <= 40: 
    		predicates['battery'] = 'Safety'
    	elif percentage < 20:
    		predicates['battery'] = 'Critical'
    	else:
    		predicates['battery'] = 'Unspecified'
    		
    elif message['topic'] == "agLand":
    	landingMode = str(message['agLand'])
    	if landingMode == 'safetyLanding':
    		predicates['landingMode'] = 'Safety'
    	elif landingMode == 'criticalLanding':
    		predicates['landingMode'] = 'Critical'
    	else:
    		predicates['landingMode'] = 'Unspecified'

    elif message['topic'] == 'cmd_vel':
    	linearY = float(message['linear']['y'])
    	predicates['forwardMotion'] = (linearY >= 0)
    	
    #print(predicates)
    return predicates
