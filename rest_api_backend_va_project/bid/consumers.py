import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


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

    async def disconnect(self, close_code):
        print('Disconnect (consumer - Bid)')
        await self.channel_layer.group_discard(
            self.bid_group_name,
            self.channel_name
        )

    async def bid(self, event):
        print('bid (consumer - Bid)')
        await self.send(text_data=json.dumps({
            'message_to_room': event
        }))
