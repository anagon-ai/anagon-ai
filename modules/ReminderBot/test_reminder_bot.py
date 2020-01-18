from unittest.mock import MagicMock

from core.events import TextInput
from modules.ReminderBot.module import ReminderBot, TimedReminderCreated, TimeInterval, TimeUnit


def test_a_minute() -> None:
    # events = []
    bot = ReminderBot()
    publish = MagicMock()
    bot.attach(publish=publish)
    bot.handler(TextInput('remind me in a minute to feed the cat'))

    publish.assert_called_with(TimedReminderCreated('feed the cat', TimeInterval(1, TimeUnit.MINUTE)))
    # assert TimedReminderCreated('feed the cat', Offset(1, TimeUnit.SECOND)) in events
