from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class BidConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('Connect (consumer - Bid)')
        self.id_ad = self.scope['url_route']['kwargs']['ad']  # ad_id
        self.bid_group_name = 'ad_%s' % self.id_ad  # chat_(id_room)
        
        await self.accept()
        await self.channel_layer.group_add(
            self.bid_group_name, 
            self.channel_name
        )
        print(f"Added {self.channel_name} channel to bid")

    async def disconnect(self, close_code):
        print('Disconnect (consumer - Bid)')
        await self.channel_layer.group_discard(
            self.bid_group_name, 
            self.channel_name
        )
        print(f"Removed {self.channel_name} channel to bid")

    async def bid(self, event):
        print('bid (consumer - Bid)')
        print('event (consumer) ==> ', event)
        await self.send(text_data=json.dumps({
            'message_to_room': event
        }))
        print(f"Got message {event} at {self.channel_name}")