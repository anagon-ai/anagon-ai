import asyncio
import datetime

from core.events import TextInput, TextOutput
from modules.BaseModule import BaseModule


class TimeBot(BaseModule):

    def boot(self) -> None:
        self.subscribe(handler=self.handle, types=TextInput)
        self.add_task(self.announce_time_every_hour())

    def handle(self, event: TextInput) -> None:
        if event.text.find('time') > -1:
            self.announce_time()

    async def announce_time_every_hour(self) -> None:
        while True:
            time = datetime.datetime.now()
            if time.minute == 0 and time.second == 0:
                self.announce_time()

            # sleep till the next minute
            await asyncio.sleep(60 - time.second)

    def announce_time(self) -> None:
        self.publish(TextOutput(text='The time is: %s' % datetime.datetime.now().strftime('%H:%M:%S')))
