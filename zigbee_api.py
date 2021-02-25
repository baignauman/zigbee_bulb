import paho.mqtt.client as mqtt
import threading
import flask
from flask import render_template, request, url_for, flash, redirect
import json
import time
global message
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def on_message(client, userdata, msg):
    global message
    message = (msg.payload)
    print(msg.topic + " " + str(msg.payload))


def thread_subscribe(client, topic_lst):
    for topic in topic_lst:
        client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()


@app.route('/', methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        app.config['switch'] = request.form['switch']
        app.config['brightness'] = request.form['brightness']
        if request.form['switch'] == '':
            return render_template('main.html')
        if request.form['switch'] =='1':
           return redirect(url_for('on'))
        if request.form['switch'] =='0':
           return redirect(url_for('off'))
        else:
            return render_template('main.html')
    if request.method == 'GET':
        try:
            app.config['state']
            app.config['brightness']
            return render_template('main.html', state=app.config['state'], brightness=app.config['brightness'])
        except:
            return render_template('main.html')


@app.route('/on', methods=['GET'])
def on():
    client = mqtt.Client()
    client.connect("192.168.178.7")
    #----daemon thread configured
    log_val_list = ["zigbee2mqtt/bulb"]
    d = threading.Thread(name='daemon', target=thread_subscribe, args=[client, log_val_list])
    d.setDaemon(True)
    d.start()
#---------------------------
    if app.config['brightness'] == '':
        app.config['brightness'] = '100'
    client.publish("zigbee2mqtt/bulb/set", '{"state":"ON"}')
    client.publish("zigbee2mqtt/bulb/set", json.dumps({"brightness":app.config['brightness']}))
    global message
    try:
        time.sleep(0.1)
        message
        message_dict = json.loads(message.decode())
        app.config['state'] = message_dict['state']
        app.config['brightness'] = message_dict['brightness']
        
        return redirect(url_for('main'))
    except:
        return "<h1>No feedback</p>"
        pass


@app.route('/off', methods=['GET'])
def off():
    client = mqtt.Client()
    client.connect("192.168.178.7")
    #----daemon thread configured
    log_val_list = ["zigbee2mqtt/bulb"]
    d = threading.Thread(name='daemon', target=thread_subscribe, args=[client, log_val_list])
    d.setDaemon(True)
    d.start()
    client.publish("zigbee2mqtt/bulb/set", '{"state":"OFF"}')
    global message
    try:
        time.sleep(0.1)
        message
        message_dict = json.loads(message.decode())
        app.config['state'] = message_dict['state']
        app.config['brightness'] = message_dict['brightness']
        return redirect(url_for('main'))
    except:
        return "<h1>No feedback</p>"
        pass




if __name__ == "__main__":
    app.run(host="192.168.178.56", port=5000, debug=True)
    