from unittest.mock import MagicMock

from core.events import TextInput
from modules.ReminderBot.module import ReminderBot, TimedReminderCreated, TimeInterval, TimeUnit, Reminder


def test_a_minute() -> None:
    # events = []
    bot = ReminderBot()
    publish = MagicMock()
    bot.attach(publish=publish)
    bot.on_text_input(TextInput('remind me in a minute to feed the cat'))

    publish.assert_called_with(TimedReminderCreated(Reminder('feed the cat'), TimeInterval(1, TimeUnit.MINUTE)))
