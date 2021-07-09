from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class NoseyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('Connect (consumer)')
        await self.accept()
        await self.channel_layer.group_add("gossip", self.channel_name)
        print(f"Added {self.channel_name} channel to gossip")

    async def disconnect(self, close_code):
        print('Disconnect (consumer)')
        await self.channel_layer.group_discard("gossip", self.channel_name)
        print(f"Removed {self.channel_name} channel to gossip")

    async def user_gossip(self, event):
        print('user_gossip (consumer)')
        print('event (consumer) ==> ', event)
        await self.send(text_data=json.dumps({
            'message_to_room': event
        }))
        print(f"Got message {event} at {self.channel_name}")
