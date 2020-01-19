from dataclasses import dataclass

from core.events import BaseEvent, TextInput, TextOutput
from core.messaging import Metadata
from modules.BaseModule import BaseModule


@dataclass
class ExampleEvent(BaseEvent):
    type = 'anagon.ai.template_module_namespace.example_event'
    content: str


class TemplateModule(BaseModule):
    def boot(self) -> None:
        """ Subscribe to relevant events here. """
        self.subscribe(self.handler, TextInput)

    def handler(self, event: TextInput, metadata: Metadata) -> None:
        self.publish(TextOutput("TextInput with id %(id)s received: %(text)s" % dict(text=event.text, id=metadata.id)))
        self.publish(ExampleEvent('example content'))

