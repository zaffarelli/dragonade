import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ParallaxConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'parallax'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        if type=="reveal":
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'parallax_reveal',
                    'message': message
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'parallax_message',
                    'message': message
                }
            )

    def parallax_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'select',
            'message': message
        }))

    def parallax_reveal(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'reveal',
            'message': message
        }))
