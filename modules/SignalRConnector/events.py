from dataclasses import dataclass

from core.events import BaseEvent


@dataclass
class SignalRConnected(BaseEvent):
  type = 'be.anagon.ai.signalr.connected'
  client_name: str

@dataclass
class SignalRDisconnected(BaseEvent):
  type = 'be.anagon.ai.signalr.disconnected'
  client_name: str