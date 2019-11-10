from websocket import create_connection
from imageai.Detection import ObjectDetection
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import os
import cv2
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
detector.loadModel()

def on_connect(client, userdata, flags, rc):
    
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensor/distance")

def on_message(client, userdata, msg):
    get_image()

def get_image(): 
    ws = create_connection("ws://10.0.202.5/service")
    data =  ws.recv()

    img = base64.b64decode(data.split(',')[1]); 
    npimg = np.frombuffer(img, dtype=np.uint8); 
    source = cv2.imdecode(npimg, 1)

    detections = detector.detectObjectsFromImage(input_image=source, input_type="array", output_image_path=os.path.join(execution_path , "image2new.jpg"), minimum_percentage_probability=30)

    """for eachObject in detections:
        print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
        print("--------------------------------")"""

    objects_list = [obj['name'] for obj in detections]
    objects_without_duplicates = list(dict.fromkeys(objects_list))

    objects = ", ".join(objects_without_duplicates)
    
    print(objects)
    publish.single("audio/objects", objects, hostname="tailor.cloudmqtt.com", port=17599, auth={'username':"test", 'password':"1234"})

    ws.close()

client = mqtt.Client()
client.username_pw_set('test', password='1234')
client.on_connect = on_connect
client.on_message = on_message

client.connect("tailor.cloudmqtt.com", 17599)
client.loop_forever()