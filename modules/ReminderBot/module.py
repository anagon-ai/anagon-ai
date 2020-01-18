import asyncio
import enum
import re
from dataclasses import dataclass

from inflection import singularize

from core.events import BaseEvent, TextInput, TextOutput
from modules.BaseModule import BaseModule


@dataclass
class TimedReminderCreated(BaseEvent):
    type = 'anagon.ai.core.poc.reminder.timed.created'
    reminder: 'Reminder'
    interval: 'TimeInterval'


@dataclass
class Reminder(BaseEvent):
    type = 'anagon.ai.core.poc.reminder.timed.triggered'
    content: str


class TimeUnit(enum.Enum):
    SECOND = 'second',
    MINUTE = 'minute',
    HOUR = 'hour',
    DAY = 'day',
    MONTH = 'month',
    YEAR = 'year'


@dataclass
class TimeInterval:
    value: int
    unit: TimeUnit

    @property
    def in_seconds(self) -> int:
        seconds_per_unit = {
            TimeUnit.SECOND: 1,
            TimeUnit.MINUTE: 60,
            TimeUnit.HOUR: 60 * 60,
            TimeUnit.DAY: 60 * 60 * 24,
            TimeUnit.MONTH: 60 * 60 * 24 * 365 // 12,
            TimeUnit.YEAR: 60 * 60 * 24 * 265,
            }
        return self.value * seconds_per_unit[self.unit]


class ReminderBot(BaseModule):
    def boot(self) -> None:
        self.subscribe(self.on_text_input, TextInput)
        self.subscribe(self.on_reminder_created, TimedReminderCreated)
        self.subscribe(self.on_reminder, Reminder)

    def on_text_input(self, event: TextInput) -> None:
        timed_reminder_match = re.search(
            '^remind me in '
            '((?P<value>(a|one|\\d+)) ?(?P<unit>seconds?|minutes?|hours?|days?|months?|s|m|h)) to (?P<content>.+)$',
            event.text)
        if timed_reminder_match:
            value = int(timed_reminder_match.group('value')
                        .replace('a', '1')
                        .replace('one', '1'))
            full_unit = timed_reminder_match.group('unit') \
                .replace('s', 'second') \
                .replace('m', 'minute') \
                .replace('h', 'hour')

            unit = TimeUnit[singularize(full_unit).upper()]

            content = timed_reminder_match.group('content')
            reminder = Reminder(content=content)
            interval = TimeInterval(value=value, unit=unit)
            self.publish(TimedReminderCreated(reminder=reminder, interval=interval))

    async def on_reminder_created(self, event: TimedReminderCreated) -> None:
        await asyncio.sleep(event.interval.in_seconds)
        self.publish(event.reminder)

    def on_reminder(self, event: Reminder) -> None:
        self.publish(TextOutput(text=f'Reminder: {event.content}'))
