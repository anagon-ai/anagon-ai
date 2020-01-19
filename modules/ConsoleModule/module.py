import asyncio
import re
from asyncio import FIRST_COMPLETED, Future
from typing import Any, List

import prompt_toolkit
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.patch_stdout import patch_stdout

from core.events import ExitCommand, TextCommand, TextCommandInfo, TextInput, TextOutput
from modules.BaseModule import BaseModule


class ConsoleModule(BaseModule):
    shutdown: Future
    session: PromptSession[Any]
    words: List[str]

    def __init__(self) -> None:
        super().__init__()
        self.shutdown = asyncio.get_event_loop().create_future()
        self.words = []

    def boot(self) -> None:
        self.session = prompt_toolkit.PromptSession(
            history=InMemoryHistory(),
            completer=WordCompleter(words=self.words)
            )

        self.subscribe(self.handle_input, types=TextInput)
        self.subscribe(self.output, types=TextOutput)
        self.subscribe(self.handle_command, types=TextCommand)
        self.subscribe(self.handle_exit, types=ExitCommand)
        self.subscribe(self.handle_text_command_info, types=TextCommandInfo)

        self.add_task(self.input_loop())
        self.add_task(self.register_commands())

    async def register_commands(self) -> None:
        self.publish(TextCommandInfo(command='exit', description='Exit the AI'))

    async def input_loop(self) -> None:
        while True:
            with patch_stdout():
                prompt_task = asyncio.create_task(self.session.prompt_async(FormattedText([('#ffffff', '> ')])))
                await asyncio.wait({prompt_task, self.shutdown}, return_when=FIRST_COMPLETED)

                if self.shutdown.done():
                    break

                if prompt_task.done():
                    text = prompt_task.result()
                    self.publish(TextInput(text=text))

    # noinspection PyMethodMayBeStatic
    def output(self, event: TextOutput) -> None:
        with patch_stdout():
            print_formatted_text(FormattedText([('#00aa66', event.text)]))

    def handle_input(self, event: TextInput) -> None:
        if event.text.startswith('/'):
            tokens = re.split('\\s+', event.text[1:])
            command = tokens[0]
            arguments = tokens[1:]
            self.publish(TextCommand(command=command, args=arguments))

    def handle_command(self, event: TextCommand) -> None:
        if event.command == 'exit':
            self.publish(ExitCommand())

    def handle_exit(self) -> None:
        self.publish(TextOutput('Exiting...'))
        self.shutdown.set_result(True)

    def handle_text_command_info(self, event: TextCommandInfo) -> None:
        self.words.append(f'/{event.command}')
