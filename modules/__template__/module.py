from core.events import TextInput, TextOutput
from core.messaging import Metadata
from modules.BaseModule import BaseModule


class TemplateModule(BaseModule):
    def boot(self) -> None:
        self.subscribe(self.handler, TextInput)

    def handler(self, event: TextInput, metadata: Metadata) -> None:
        self.publish(TextOutput("TextInput with id %(id)s received: %(text)s" % dict(text=event.text, id=metadata.id)))
