# Requires websocket-client

import json
from websocket import create_connection


class OpenSpaceAPI:

    def __init__(self, host='localhost', port=4682):
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        self._ws = create_connection(f"ws://{self.host}:{self.port}/websocket")

    def send_json(self, data):
        print(json.dumps(data).encode('ascii'))
        self._ws.send(json.dumps(data).encode('ascii'))


message1 = {'topic': 1,
            'type': 'subscribe',
            'payload': {'event': 'start_subscription',
                        'property': 'Scene.Earth.Scale.Scale'}}


message2 = {'topic': 2,
            'type': 'set',
            'payload': {'value': 1.0,
                        'property': 'Scene.Earth.Scale.Scale'}}

message3 = {"topic":4,
            "type": "luascript",
            "payload": {"function": "openspace.addSceneGraphNode",
                        "arguments":[{"Identifier": "ExampleSphere5",
                                      "Parent": "Earth",
                                      "Transform":{"Translation":{"Type":"GlobeTranslation",
                                                                  "Globe":"Earth",
                                                                  "Latitude":0,
                                                                  "Longitude":0,
                                                                  "FixedAltitude":10}},
                                                   "Renderable":{"Type":"RenderableSphere",
                                                                 "Enabled":True,
                                                                 "Size":200000,
                                                                 "Segments":20,
                                                                 "Opacity":1,
                                                                 "Texture":
                                                                 "${DATA}/test2.jpg",
                                                                 "Orientation":"Both"},
                                                   "GUI":{"Name":"ExampleSphere5",
                                                   "Path":"/Other/Spheres"}}],
                        "return":False}}


api = OpenSpaceAPI()
# api.send_json(message1)
# api.send_json(message2)

from astropy.table import Table
table = Table.read('earthquakes_2010.csv')
print(table.colnames)

import uuid

import numpy as np
index = np.random.randint(0, len(table), 200)

for row in table[index]:

    message3['payload']['arguments'][0]['Identifier'] = str(uuid.uuid4())
    message3['payload']['arguments'][0]['Transform']['Translation']['Longitude'] = row['longitude']
    message3['payload']['arguments'][0]['Transform']['Translation']['Latitude'] = row['latitude']

    api.send_json(message3)
