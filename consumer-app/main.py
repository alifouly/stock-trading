import paho.mqtt.client as mqtt
from decouple import config

# Callback Function on Connection with MQTT Server
def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    client.subscribe(config('MQTT_TOPIC'))

# Callback Function on Receiving the Subscribed Topic/Message
def on_message( client, userdata, msg):

	print(msg.payload.decode("utf-8"))
	#################################################################################################################################################
	# Here we should implement that on receiving/consuming data from the stream we should update our database stocks table
	# if the consumed stock ID exists in the DB, so we should update its info (price, availability) OR create a new row if it does not exist
	#################################################################################################################################################


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config('MQTT_HOST'), int(config('MQTT_PORT')), 60)

client.loop_forever()