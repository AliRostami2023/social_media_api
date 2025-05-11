import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ActivityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f'activity_{self.user.id}' 
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()


    async def disconnect(self, close_code):
        if not self.user.is_anonymous:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def receive(self, text_data):
        pass

    async def send_activity(self, event):
        await self.send(text_data=json.dumps({
            'activity_type': event['activity_type'],
            'user': event['user'],
            'post_id': event.get('post_id'),
            'comment_id': event.get('comment_id'),
            'viewed_page': event.get('viewed_page'),
        }))

