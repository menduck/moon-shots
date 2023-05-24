import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from channels.db import database_sync_to_async
from musics.models import Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = await self.get_room()

        # 그룹 참가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # 이전 채팅들 전송
        await self.send_existing_chat_messages()


    # 사용자가 속한 채팅방(Room)을 가져옴
    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(pk=self.room_name)


    # db에서 해당 채팅방의 이전 메시지들 가져옴
    @database_sync_to_async
    def get_existing_chat_messages(self):
        return ChatMessage.objects.filter(room=self.room).order_by("timestamp")


    # 가져온 이전 채팅 내용을 클라이언트로 전송
    async def send_existing_chat_messages(self):
        # Get existing chat messages for the room from the database
        chat_messages = await self.get_existing_chat_messages()

        # Send each chat message to the user
        for chat_message in chat_messages:
            await self.send(text_data=json.dumps({
                "message": chat_message.content,
                "user": chat_message.user.username,
                # "timestamp": chat_message.timestamp.isoformat(),
            }))


    # 클라이언트가 웹소켓 연결 끊었을 때 채팅방 그룹에서 클라 제거
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    # 클라이언트에서 메시지 전송 시 호출
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]  # 메시지 추출
        user = self.scope["user"]  # 인증된 사용자 가져오기

        await self.save_chat_message(user, message)  # 비동기 데이터베이스 작업 호출

        #  self.room_group_name에 해당하는 채팅방에 속한 클라이언트들에게 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",  # chat_message 호출
                "message": message,
                "user": user.username,
                # "timestamp": chat_message.timestamp.isoformat(),
            }
        )


    # 받은 메시지 db에 저장, 비동기적으로 작업 수행
    @database_sync_to_async
    def save_chat_message(self, user, message):
        chat_message = ChatMessage(user=user, content=message, room=self.room)
        chat_message.save()


    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        # timestamp = event["timestamp"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            # "timestamp": timestamp,
            })
        )
