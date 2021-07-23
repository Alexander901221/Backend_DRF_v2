import json
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async

from .models import Chat, Room
from user.models import User


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('Connect (consumer - Chat)')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        await self.check_user()  # Check user authentication

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('Disconnect (consumer - Chat)')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('receive (consumer - Chat)')
        new_message = await self.create_message(text_data)

        data = {
            'username': new_message.user.username,
            'id': new_message.user.pk,
            'created_at': new_message.date.strftime('%Y-%m-%d %H:%m'),
            'text': new_message.text,
            'photo': '/images/' + str(new_message.user.photo)
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': [data]
            }
        )

    async def chat_message(self, event):
        print('chat_message (consumer - Chat)')
        message = event['message']

        await self.send(text_data=json.dumps({
            'message_to_room': message
        }))

    @database_sync_to_async
    def create_message(self, text):
        print('create_message (consumer - Chat)')
        room = Room.objects.get(pk=self.room_name)
        user = User.objects.get(pk=self.user.pk)
        create_new_message = Chat.objects.create(
            room=room,
            user=user,
            text=text,
        )

        return create_new_message

    @database_sync_to_async
    def check_user(self):  # Check user authentication and exists in the room
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")

        user_in_room = Room.objects.filter(Q(pk=self.room_name) & Q(invited__pk=self.user.pk)).exists()

        if not user_in_room:
            raise DenyConnection('Пользователя нет в данной комнате')
