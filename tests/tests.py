import unittest
from dataclasses import dataclass
from typing import Union
from uuid import UUID

from jsonpickle import Pickler

from core.core import Core
from core.errors import CoreNotBootedError, ModuleError, ModulePublishedBadEventError, ModuleSubscribedToNonClassError, \
    ModuleSubscribedToNonEventClassError
from core.events import BaseEvent
from core.messaging import Metadata
from modules.BaseModule import BaseModule

test_uuid = UUID('24415436-3319-11ea-964d-88e9fe73dff3')


@dataclass
class EventTypeA(BaseEvent):
    content: str
    type = 'be.anagon.ai.core.poc.a'


@dataclass
class EventTypeB(BaseEvent):
    content: str
    type = 'be.anagon.ai.core.poc.b'


@dataclass
class TestEvent(BaseEvent):
    type = 'be.anagon.ai.test.event'
    content: str

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
        class AEventsModule(BaseModule):
            received_events = []

            def boot(self):
                self.subscribe(self.handle_a, types=EventTypeA)

            def handle_a(self, event: EventTypeA):
                self.received_events.append(event.content)

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

        self.assertEqual({'type': 'foo', 'attr': 'bar', 'text': 'hello'}, TestEvent('hello').dict)

    def test_handle_metadata(self):
        received_ids = []

        class MetadataModule(BaseModule):
            def boot(self):
                self.subscribe(self.handler)

            def handler(self, event: BaseEvent, metadata: Metadata):
                received_ids.append(metadata.id)

        ai = Core(metadata_provider=lambda: Metadata(id=test_uuid))
        ai.add_module(MetadataModule())
        ai.boot()

        ai.publish(TestEvent('hello'))

        self.assertEqual([test_uuid], received_ids)

    def test_metadata_id_is_same_for_all_handlers(self):
        received_ids = []

        class MetadataModule(BaseModule):
            def boot(self):
                self.subscribe(lambda metadata: received_ids.append(metadata.id))
                self.subscribe(lambda metadata: received_ids.append(metadata.id))

        ai = Core()
        ai.add_module(MetadataModule())
        ai.boot()

        ai.publish(TestEvent('hello'))

        self.assertEqual(2, len(received_ids))
        self.assertEqual(received_ids[0], received_ids[1])

    def test_handler_arguments(self):
        class FooModule(BaseModule):
            def boot(self):
                self.subscribe(self.handle)

            def handle(self, message):
                pass

        ai = Core()
        ai.add_module(FooModule())

        self.assertRaises(ModuleError, lambda: ai.boot())

    def test_pickle_json_includes_class_attributes(self):
        @dataclass
        class TestEventClassAttributes(BaseEvent):
            type = 'ai.anagon.base'
            sub_type = 'ai.anagon.child'
            content: str

        self.assertEqual({
            'type': 'ai.anagon.base',
            'sub_type': 'ai.anagon.child',
            'content': 'test',
            }, Pickler(unpicklable=False).flatten(TestEventClassAttributes("test")))

    def test_handler_type_matches_subscribe(self):
        class ModuleWithTypeMismatch(BaseModule):

            def boot(self) -> None:
                self.subscribe(self.handle, types=EventTypeA)

            def handle(self, event: EventTypeB):
                pass

        ai = Core()
        ai.add_module(ModuleWithTypeMismatch())

        self.assertRaises(ModuleError, lambda: ai.boot())

    def test_handler_multiple_types(self):
        class ModuleWithMultipleTypes(BaseModule):

            def boot(self) -> None:
                self.subscribe(self.handle, types=[EventTypeA, EventTypeB])

            def handle(self, event: Union[EventTypeA, EventTypeB]):
                pass

        ai = Core()
        ai.add_module(ModuleWithMultipleTypes())
        ai.boot()

    def test_handler_without_type_hint(self):
        class ModuleWithMultipleTypes(BaseModule):

            def boot(self) -> None:
                self.subscribe(self.handle, types=[EventTypeA, EventTypeB])

            def handle(self, event):
                pass

        ai = Core()
        ai.add_module(ModuleWithMultipleTypes())
        ai.boot()