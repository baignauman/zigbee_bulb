import requests
import json
import zigbee_api


def turn_on():
    x = requests.get('http://0173808fe6a8.ngrok.io/on')
    assert 200 == x.status_code

def turn_off():
    x = requests.get('http://0173808fe6a8.ngrok.io/off')
    assert 200 == x.status_code