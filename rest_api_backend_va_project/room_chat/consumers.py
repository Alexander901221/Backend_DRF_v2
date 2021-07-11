import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from .models import Chat, Room
from user.models import User


class ChatConsumer(AsyncJsonWebsocketConsumer):
    # Присоединение к комнате
    async def connect(self):
        print('CONNECT')
        self.room_name = self.scope['url_route']['kwargs']['room_name']  # id_room
        self.room_group_name = 'chat_%s' % self.room_name  # chat_(id_room)
        self.user = self.scope["user"]

        await self.check_user()  # Проверка user на авторизацию и, на то что он есть в этой комнате

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # Отсоединение
    async def disconnect(self, close_code):
        print('DISCONNECT')
        # Покинуть группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщения от WebSocket
    async def receive(self, text_data):
        print('RECEIVE')
        new_message = await self.create_message(text_data)

        data = {
            'author': new_message.user.username,
            'created_at': new_message.date.strftime('%Y-%m-%d %H:%m'),
            'text': new_message.text
        }
        # Отправить сообщение в комнату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': [data]
            }
        )

    # Получение сообщения от группы
    async def chat_message(self, event):
        print('CHAT_MESSAGE')
        message = event['message']

        # Отправить сообщение в WebSocket
        await self.send(text_data=json.dumps({
            'message_to_room': message
        }))
    
    async def onopen(self):
        print('self -> ', self)

    @database_sync_to_async  # Чтобы мы могли обращаться к базе внутри функции
    def create_message(self, text):
        print('CREATE_MESSAGE')
        room = Room.objects.get(pk=self.room_name)
        user = User.objects.get(pk=self.user.pk)
        create_new_message = Chat.objects.create(
            room=room,
            user=user,
            text=text,
        )

        return create_new_message

    @database_sync_to_async
    def check_user(self):  # Проверка user на авторизованного и на существование в комнате
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")

        user_in_room = Room.objects.filter(Q(pk=self.room_name) & Q(invited__pk=self.user.pk)).exists()
        print('user_in_room --> ', user_in_room)

        if not user_in_room:
            raise DenyConnection('Пользователя нет в данной комнате')

