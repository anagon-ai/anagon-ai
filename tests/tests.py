import unittest
from dataclasses import dataclass

from core.core import Core
from core.events import BaseEvent
from core.errors import CoreNotBootedError, ModulePublishedBadEventError
from modules.BaseModule import BaseModule


@dataclass
class EventTypeA(BaseEvent):
  content: str
  type = 'be.anagon.ai.core.poc.a'


@dataclass
class EventTypeB(BaseEvent):
  content: str
  type = 'be.anagon.ai.core.poc.b'


class AEventsModule(BaseModule):
  received_events = []

  def boot(self):
    self.subscribe(self.handle_a, types=EventTypeA.type)

  def handle_a(self, event: EventTypeA):
    self.received_events.append(event.content)

class AllEventsModule(BaseModule):
  received_events = []

  def boot(self):
    self.subscribe(handler=self.handle)

  def handle(self, event):
    self.received_events.append(event.content)

class CoreTests(unittest.TestCase):
  def test_ai_must_be_booted_before_publishing(self):
    ai = Core()
    self.assertRaises(CoreNotBootedError, lambda: ai.publish(EventTypeA(content="a")))

  def test_module_receives_only_events_it_subscribed_to(self):
    ai = Core()
    foobar = AEventsModule()
    ai.add_module(foobar)

    ai.boot()

    ai.publish(EventTypeA(content="a"))
    ai.publish(EventTypeB(content="b"))

    self.assertEqual(['a'], foobar.received_events)

  def test_module_receives_all_events(self):
    ai = Core()
    module = AllEventsModule()
    ai.add_module(module)

    ai.boot()

    ai.publish(EventTypeA(content="a"))
    ai.publish(EventTypeB(content="b"))

    self.assertEqual(['a', 'b'], module.received_events)

  def test_publishing_non_event(self):
    class BadPublisher(BaseModule):

      def boot(self):
        pass

    ai = Core()
    module = BadPublisher()
    ai.add_module(module)

    ai.boot()

    self.assertRaises(ModulePublishedBadEventError, lambda: module.publish("not an event"))