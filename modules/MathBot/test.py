from typing import List, Any
from unittest import TestCase

from core.core import Core
from core.events import TextInput, BaseEvent, TextOutput
from modules.BaseModule import BaseModule
from modules.MathBot.module import MathBot, MathParsed, Addition, Constant


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

    def test_detect_expressions_from_text_input(self):
        bot = MathBot()
        events = []
        setattr(bot, 'publish', lambda event: events.append(event))

        bot.handle_text(TextInput('10+2'))

        self.assertEqual([MathParsed(Addition(Constant(10), Constant(2)))], events)

    def test_output_expression_result(self):
        class TestHelperBot(BaseModule):
            events: List[BaseEvent]

            def boot(self) -> None:
                self.events = []
                self.subscribe(lambda event: self.events.append(event))

        helper = TestHelperBot()
        bot = MathBot()

        ai = Core()
        ai.add_module(bot)
        ai.add_module(helper)
        ai.boot()
        ai.publish(TextInput('10+2'))

        self.assertIn(MathParsed(Addition(Constant(10), Constant(2))), helper.events)
        self.assertIn(TextOutput('The result is: 12.0'), helper.events)


