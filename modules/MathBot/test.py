from unittest import TestCase

from core.events import TextInput
from modules.MathBot.module import MathBot


class TestMathBot(TestCase):
    @staticmethod
    def run_bot(assignment: str) -> str:
        bot = MathBot()
        local_event_bus = []
        setattr(bot, 'publish', lambda event: local_event_bus.append(event))

        bot.handle_text(TextInput(assignment))
        bot.execute(local_event_bus.pop())

        return local_event_bus.pop().text

    def test_constant(self):
        self.assertEqual(
            'The result is: 5.0',
            self.run_bot('5')
        )

    def test_addition(self):
        self.assertEqual(
            'The result is: 10.0',
            self.run_bot('3+7')
        )

    def test_multiple_additions(self):
        self.assertEqual(
            'The result is: 15.0',
            self.run_bot('3+7+5')
        )

    def test_not_math(self):
        self.assertEqual(
            'The result is: nan',
            self.run_bot('This is not a calculation')
        )

    def test_not_math_but_with_plus_sign(self):
        self.assertEqual(
            'The result is: nan',
            self.run_bot('This is not a calculation + it contains a plus sign')
        )
