import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *




class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room = await Chat.objects.filter(id=self.chat_id).afirst()
        self.messages = []
        
        if not self.room:
            data={'users':{}}
            data['users']=[{'username': self.scope['username']}]
            await Chat.objects.acreate(**data)
        
        self.room_group_name = f'chat_{self.room.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #print(self.scope['headers'])
        data={}
        data['chat_id']=self.room
        data['message']={'user': 'user_applicant', 'body': message}
        await Messages.objects.acreate(**data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    