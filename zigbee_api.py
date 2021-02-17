import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import threading
import flask
import json
import time
global message
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def on_message(client,userdata,msg):
        global message
        message=(msg.payload)
        print(msg.topic+" "+str(msg.payload))


def thread_subscribe(client,topic_lst):
    for topic in topic_lst:
        client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()
        

@app.route('/on', methods=['GET'])
def on():
    client=mqtt.Client()
    client.connect("192.168.178.7")
    #----daemon thread configured
    log_val_list=["zigbee2mqtt/bulb"]
    d=threading.Thread(name='daemon',target=thread_subscribe,args=[client,log_val_list])
    d.setDaemon(True)
    d.start()
#---------------------------
    client.publish("zigbee2mqtt/bulb/set", '{"state":"ON"}')
    #client.publish("zigbee2mqtt/bulb/set", '{"brightness":"150"}')
    global message
    try:
        time.sleep(0.1)
        message
        message_dict=json.loads(message.decode())
        return "<h1>State: {}</p>".format(message_dict['state'])
    except:
        return "<h1>No feedback</p>"

@app.route('/off', methods=['GET'])
def off():
    client=mqtt.Client()
    client.connect("192.168.178.7")
    #----daemon thread configured
    log_val_list=["zigbee2mqtt/bulb"]
    d=threading.Thread(name='daemon',target=thread_subscribe,args=[client,log_val_list])
    d.setDaemon(True)
    d.start()
    
    client.publish("zigbee2mqtt/bulb/set", '{"state":"OFF"}')
    global message
    try:
        time.sleep(0.1)
        message
        message_dict=json.loads(message.decode())
        return "<h1>State: {}</p>".format(message_dict['state'])
    except:
        return "<h1>No feedback</p>"
if __name__ == "__main__":
    app.run(host="192.168.178.56", port=5000, debug=True)    

    
