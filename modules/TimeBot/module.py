import asyncio
import datetime

from core.events import ExitCommand, TextInput, TextOutput, TextCommandInfo
from modules.BaseModule import BaseModule


class TimeBot(BaseModule):
    running: bool

    def __init__(self) -> None:
        self.running = True

    def boot(self) -> None:
        self.subscribe(self.on_text_input, types=TextInput)
        self.subscribe(self.on_exit, types=ExitCommand)
        self.add_task(self.announce_time_every_hour())
        self.add_task(self.register_commands())

    def on_text_input(self, event: TextInput) -> None:
        if event.text.find('time') > -1:
            self.announce_time()

    async def announce_time_every_hour(self) -> None:
        while self.running:
            time = datetime.datetime.now()
            if time.minute == 0 and time.second == 0:
                self.announce_time()

            await asyncio.sleep(min(5, 60 - time.second))

    async def register_commands(self) -> None:
        self.publish(TextCommandInfo('time', 'Show the time'))

    def announce_time(self) -> None:
        self.publish(TextOutput(text='The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S')))

    def on_exit(self) -> None:
        self.running = False
