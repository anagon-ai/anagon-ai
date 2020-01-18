import asyncio
import datetime

from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class TimeBot(BaseModule):

    def boot(self) -> None:
        self.subscribe(handler=self.handle, types=TextInput)
        self.add_task(self.announce_time_every_minute())

    def handle(self, event: TextInput) -> None:
        if event.text.find('time') > -1:
            self.announce_time()

    async def announce_time_every_minute(self) -> None:
        while True:
            time = datetime.datetime.now()
            if time.second == 0:
                self.announce_time()

            await asyncio.sleep(1)

    def announce_time(self) -> None:
        self.publish(TextOutput(text='The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S')))
