import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.auth import login , get_user

class ChatConsumer(WebsocketConsumer):


    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        print('consumers',self.user)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('recive_func')
        print(async_to_sync(get_user)(self.scope))
        print(text_data_json)
        print('message : is  ', text_data_json['message'])