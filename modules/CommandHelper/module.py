from typing import List

from core.events import TextCommand, TextCommandInfo, TextOutput
from modules.BaseModule import BaseModule


class CommandHelper(BaseModule):
    commands: List[TextCommandInfo]

    def __init__(self) -> None:
        super().__init__()
        self.commands = []

    def boot(self) -> None:
        self.subscribe(self.on_command, TextCommand)
        self.subscribe(self.on_text_command_info, TextCommandInfo)
        self.add_task(self.register_commands())

    async def register_commands(self) -> None:
        self.publish(TextCommandInfo(command='help', description='Show available commands'))

    def on_command(self, event: TextCommand) -> None:
        if event.command == 'help':
            for command in self.commands:
                self.publish(TextOutput(f'/{command.command.ljust(20)} {command.description}'))

    def on_text_command_info(self, event: TextCommandInfo) -> None:
        if event not in self.commands:
            self.commands.append(event)
            self.commands.sort(key=lambda command: command.command)
