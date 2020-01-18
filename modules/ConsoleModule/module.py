import asyncio
from typing import Any

import prompt_toolkit
from prompt_toolkit import PromptSession, print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class ConsoleModule(BaseModule):
    session: PromptSession[Any]

    def boot(self) -> None:
        self.session = prompt_toolkit.PromptSession(history=InMemoryHistory())

        self.subscribe(handler=self.output, types=TextOutput)
        self.add_task(self.input_loop())
        self.add_task(self.print_message_later())

    async def input_loop(self) -> None:
        while True:
            with patch_stdout():
                text = await self.session.prompt_async(FormattedText([('#ffffff', '> ')]))
                self.publish(TextInput(text=text))

    async def print_message_later(self) -> None:
        await asyncio.sleep(1)
        self.publish(TextOutput('Delayed message'))

    # noinspection PyMethodMayBeStatic
    def output(self, event: TextOutput) -> None:
        with patch_stdout():
            print(FormattedText([('#00aa66', event.text)]))
