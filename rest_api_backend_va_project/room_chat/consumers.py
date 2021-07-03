import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from .models import Chat, Room


class ChatConsumer(AsyncWebsocketConsumer):
    # Присоединение к комнате
    async def connect(self):
        print('CONNECT')
        self.room_name = self.scope['url_route']['kwargs']['room_name']  # ad1
        self.room_group_name = 'chat_%s' % self.room_name  # chat_ad1
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        new_message = await self.create_message(message)

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
                'message': data
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

    @database_sync_to_async  # Чтобы мы могли обращаться к базе внутри функции
    def create_message(self, text):
        room = Room.objects.get(pk=self.room_name)
        create_new_message = Chat.objects.create(
            room=room,
            user=self.user,
            text=text,
        )

        return create_new_message

    @database_sync_to_async
    def check_user(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")

        user_in_room = Room.objects.filter(Q(pk=self.room_name) & Q(invited__username=self.user.username)).exists()

        if not user_in_room:
            raise DenyConnection('Пользователя нет в данной комнате')

