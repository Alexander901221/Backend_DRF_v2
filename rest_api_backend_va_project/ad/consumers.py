from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class AdConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('Connect (consumer - Ad)')
        self.id_user = self.scope['url_route']['kwargs']['city']
        self.ad_group_name = 'city_%s' % self.id_user
        await self.accept()
        await self.channel_layer.group_add(
            self.ad_group_name, 
            self.channel_name
        )
        print(f"Added {self.channel_name} channel to ad")

    async def disconnect(self, close_code):
        print('Disconnect (consumer - Ad)')
        await self.channel_layer.group_discard(
            self.ad_group_name, 
            self.channel_name
        )
        print(f"Removed {self.channel_name} channel to ad")

    async def ad(self, event):
        print('ad (consumer - Ad)')
        print('event (consumer) ==> ', event)
        await self.send(text_data=json.dumps({
            'message_to_room': event
        }))
        print(f"Got message {event} at {self.channel_name}")