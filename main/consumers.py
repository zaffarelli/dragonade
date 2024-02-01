import json
from channels.generic.websocket import WebsocketConsumer


class ParallaxConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are connected!'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("Message:", message)
        self.send(text_data=json.dumps({
            'type': 'info',
            'message': message
        }))
