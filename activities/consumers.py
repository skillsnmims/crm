from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
import json
from channels.layers import get_channel_layer
from django.db import IntegrityError
from .models import AgentActivity
import time
from django.utils import timezone


class AgentConsumer(JsonWebsocketConsumer):

    def connect(self):
        print("agent consumer requested!")
        user = self.scope['user']
        if user.is_authenticated and user.is_agent:
            agent = user.agent
            activity_args = {'status': 'ON', 'last_seen': timezone.now(), 'channel_name': self.channel_name}
            if hasattr(agent, "agentactivity"):
                agent_activity = agent.agentactivity
                agent_activity.status = "ON"
                agent_activity.last_seen = timezone.now()
                agent_activity.channel_name = self.channel_name
                agent_activity.save()
            else:
                agent_activity = AgentActivity.objects.create(agent=agent, **activity_args)
            async_to_sync(self.channel_layer.group_add)(
                'branch_id_' + str(agent.team.branch.id),
                self.channel_name,
            )
            print("agent consumer accepted")
            self.accept()
        else:
            self.close()

    def set_offline(self, info_dict=None):
        activity = self.scope['user'].agent.agentactivity
        if activity.status == "ON":
            activity.last_seen = timezone.now()
        activity.status = "OF"
        if info_dict is not None:
            comment = info_dict.get("comment" or "")
            activity.comment = comment
        activity.save()

    def set_break(self, info_dict):
        comment = info_dict.get("comment" or "")
        activity = self.scope['user'].agent.agentactivity
        if activity.status == "ON":
            activity.last_seen = timezone.now()
        activity.status = "BR"
        activity.comment = comment
        activity.save()

    def receive_chat_message(self, info_dict):
        try:
            async_to_sync(self.channel_layer.group_send)(
                'branch_id_' + str(self.scope['user'].agent.team.branch.id),
                {
                    "type": "chat.message",
                    'team': self.scope["user"].agent.team.name,
                    "user_type": self.scope["user"].user_type,
                    "username": self.scope["user"].email,
                    "message": info_dict['message'],
                }
            )
            print("sent")
        except Exception as e:
            print("receive chat error : ", e)
            pass

    def chat_message(self, event):
        print("chat message called")
        self.send_json(
            {
                'command': 'CHAT_MESSAGE',
                'info_dict': {
                    "team": event["team"],
                    "username": event["username"],
                    "message": event["message"],
                    "user_type": event["user_type"],
                },
            }
        )

    def receive_json(self, content, **kwargs):
        command = content.get("command", None)
        print("MSG CAME : ", content)
        if command == "SET_BREAK":
            self.set_break(content['info_dict'])
        elif command == "SET_OFFLINE":
            self.set_offline(content['info_dict'])
        elif command == 'CHAT_MESSAGE':
            self.receive_chat_message(content['info_dict'])

    def disconnect(self, close_code):
        self.set_offline()
        print("disconnected")


class BranchAdminConsumer(JsonWebsocketConsumer):

    def connect(self):
        user = self.scope['user']
        if user.is_authenticated and user.is_branch_admin:
            admin = user.branchadmin
            async_to_sync(self.channel_layer.group_add)(
                'branch_id_' + str(admin.branch.id),
                self.channel_name,
            )
            print("agent consumer accepted")
            self.accept()
        else:
            self.close()

    def receive_chat_message(self, info_dict):
        try:
            async_to_sync(self.channel_layer.group_send)(
                'branch_id_' + str(self.scope['user'].branchadmin.branch.id),
                {
                    "type": "chat.message",
                    "team": "Admin",
                    "user_type": self.scope["user"].user_type,
                    "username": self.scope["user"].email,
                    "message": info_dict['message'],
                }
            )
        except Exception as e:
            print("receive chat error : ", e)
            pass

    def chat_message(self, event):
        print("chat message called")
        self.send_json(
            {
                'command': 'CHAT_MESSAGE',
                'info_dict': {
                    "team": event["team"],
                    "username": event["username"],
                    "message": event["message"],
                    "user_type": event["user_type"],
                },
            }
        )

    def receive_json(self, content, **kwargs):
        command = content.get("command", None)
        if command == 'CHAT_MESSAGE':
            self.receive_chat_message(content['info_dict'])

    def disconnect(self, close_code):
        print("disconnected")
