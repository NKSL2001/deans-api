from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger("django")

class CrisesConsumer(WebsocketConsumer):
    def connect(self):
        """
        Perform actions on WebSocket connection start and join the 'crises' group.
        """
        try:
            async_to_sync(self.channel_layer.group_add)("crises", self.channel_name)
            self.accept()
            logger.info(f"WebSocket connected: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {str(e)}")
            self.close()

    def disconnect(self, close_code):
        """
        Perform actions on WebSocket disconnect and leave the 'crises' group.
        """
        try:
            async_to_sync(self.channel_layer.group_discard)("crises", self.channel_name)
            logger.info(f"WebSocket disconnected: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnection: {str(e)}")

    def receive(self, text_data):
        """
        Handle incoming messages from WebSocket clients.
        """
        try:
            data = json.loads(text_data)
            logger.info(f"Received data: {data}")
            # Process the message if needed
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {str(e)}")

    def crises_update(self, event):
        """
        Send messages to WebSocket clients upon receiving updates.
        """
        payload = event.get("payload", {})
        self.send(json.dumps(payload))
