import json
from Eclipse.services import *
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.auth import login , get_user


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_title = self.scope['url_route']['kwargs']['chat_title']
        self.user = self.scope["user"]
        self.username = self.user.__str__()


        # Join room group
        await self.channel_layer.group_add(
            self.chat_title,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_title,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message:
            date_time = await database_sync_to_async(add_massage)(message,self.username,self.chat_title)
            # Send message to room group
            await self.channel_layer.group_send(
                self.chat_title,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.username,
                    'date_time': date_time
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['username']
        date_time = event['date_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username' : user,
            'date_time': date_time
        }))

