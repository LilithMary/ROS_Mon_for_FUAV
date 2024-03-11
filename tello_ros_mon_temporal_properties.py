import oracle

# replace "visual_sensor" with topic for detectRed
# replace "reaction" with field name that carries 'reactRed'
# replace "batteryInfo" with topic for battery
# replace "percentage" with field name that carries 'battery'
# replace "landingMode" with field name that carries 'safetyLanding' and 'criticalLanding'

pl = [
'(once[100:101]({topic: "visual_sensor", detectRed: True}) -> {topic: "agentReact", reactRed: True} )',
'({topic: "batteryInfo", battery: "Safety"} -> {topic: "agLand", landingMode: "Safety"})',
'({topic: "batteryInfo", battery: "Critical"} -> {topic: "agLand", landingMode: "Critical"})',
'({topic: "drone1/cmd_vel", forwardMotion: True})'
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

    if message['topic'] == "visual_sensor":
    	detectRed = int(message['detectRed'])
    	predicates['detectRed'] = (detectRed > 200)
 
    elif message['topic'] == "agentReact":
    	reaction = str(message['reaction'])
    	predicates['reactRed'] = (reaction == 'reactRed')
    	
    elif message['topic'] == "batteryInfo":
    	percentage = int(message['percentage'])
    	if percentage >= 20 and percentage <= 40: 
    		predicates['battery'] = 'Safety'
    	elif percentage < 20:
    		predicates['battery'] = 'Critical'
    	else:
    		predicates['battery'] = 'Unspecified'
    		
    elif message['topic'] == "agLand":
    	landingMode = message['landingMode']
    	if landingMode == 'safetyLanding':
    		predicates['landingMode'] = 'Safety'
    	elif landingMode == 'criticalLanding':
    		predicates['landingMode'] = 'Critical'
    	else:
    		predicates['landingMode'] = 'Unspecified'

    elif message['topic'] == 'drone1/cmd_vel':
    	linearY = float(message['linear']['y'])
    	predicates['forwardMotion'] = (linearY >= 0)
    	
    #print(predicates)
    return predicates
