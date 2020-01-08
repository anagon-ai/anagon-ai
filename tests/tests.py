import unittest
from dataclasses import dataclass

from core.core import Core
from core.errors import CoreNotBootedError, ModulePublishedBadEventError, ModuleSubscribedToNonClassError, \
  ModuleSubscribedToNonEventClassError
from core.events import BaseEvent
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
    self.subscribe(self.handle_a, types=EventTypeA)

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

  def test_publishing_non_class(self):
    class BadPublisher(BaseModule):

      def boot(self):
        pass

    ai = Core()
    module = BadPublisher()
    ai.add_module(module)

    ai.boot()

    self.assertRaises(ModulePublishedBadEventError, lambda: module.publish("not an event"))

  def test_subscribing_non_class(self):
    class BadSubscriber(BaseModule):
      def boot(self):
        self.subscribe(lambda: None, types='MyEvent')

    ai = Core()
    module = BadSubscriber()
    ai.add_module(module)
    self.assertRaises(ModuleSubscribedToNonClassError, lambda: ai.boot())

  def test_subscribing_non_event_class(self):
    class FakeEvent:
      pass

    class BadSubscriber(BaseModule):
      def boot(self):
        self.subscribe(lambda: None, types=FakeEvent)

    ai = Core()
    module = BadSubscriber()
    ai.add_module(module)

    self.assertRaises(ModuleSubscribedToNonEventClassError, lambda: ai.boot())

  def test_event_dict(self):
    @dataclass
    class TestEvent(BaseEvent):
      type = 'foo'  # overwritten
      attr = 'bar'  # class attribute
      text: str

    self.assertEqual({'type': 'foo', 'attr': 'bar', 'text': 'hello'}, TestEvent('hello').as_dict)
