import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, ChatMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Access session from self.scope
        session = self.scope.get('session')

        # Retrieve user ID from session
        self.uid = session.get('logid') if session else None

        if not self.uid:
            self.close()  # Close connection if session or logid is missing
            return

        try:
            self.Authenticated = User.objects.get(id=self.uid)
        except User.DoesNotExist:
            self.close()
            return

        self.user = self.Authenticated
        self.room_name = f"user_{self.user.id}"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']

        # Save the message in the database
        sender = self.user
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return

        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)

        # Send message to receiver's group
        receiver_group_name = f"chat_user_{receiver_id}"
        async_to_sync(self.channel_layer.group_send)(
            receiver_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'Id':sender.id
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        Id = event['Id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'senderId':Id
        }))
