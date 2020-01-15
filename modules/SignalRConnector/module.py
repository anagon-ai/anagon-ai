import logging

from signalrcore.hub_connection_builder import HubConnectionBuilder

from core.events import BaseEvent, TextOutput
from modules.BaseModule import BaseModule
from modules.SignalRConnector.events import SignalRConnected, SignalRDisconnected


class SignalRConnector(BaseModule):
  connection: HubConnectionBuilder = None

  def __init__(self, hub_url):
    self.hub_url = hub_url

  def boot(self):
    logging.info("Connecting to websocket")

    self.connection = HubConnectionBuilder() \
      .with_url(self.hub_url) \
      .configure_logging(logging.DEBUG) \
      .with_automatic_reconnect(
      {
          "type": "raw",
          "keep_alive_interval": 10,
          "reconnect_interval": 5,
          "max_attempts": 5
          }
      ) \
      .build()

    self.connection.on_open(self.on_signalr_connected)
    self.connection.on_close(self.on_signalr_disconnected)
    self.connection.on('EventAdded', self.on_signalr_event)
    self.connection.start()
    self.subscribe(self.on_event)
    self.subscribe(self.handle_connected, types=SignalRConnected)

  def on_signalr_connected(self):
    self.publish(SignalRConnected('Anagon AI Bot'))

  def on_signalr_disconnected(self):
    self.publish(SignalRDisconnected('Anagon AI Bot'))

  def on_signalr_event(self, args):
    event, = args
    logging.info("Received SignalR event: %s" % event)
    if ('type', 'be.anagon.ai.signalr.connected') in event.items():
      self.publish(SignalRConnected(event['client_name']))
      pass

  def on_event(self, event: BaseEvent):
    logging.info("Passing event %s to SignalR server" % event)
    if not isinstance(event, SignalRConnected):
      self.connection.send('AddEvent', [event.as_dict])

  def handle_connected(self, event: SignalRConnected):
    self.publish(TextOutput(text='%(client_name)s connected through SignalR' % event.as_dict))
