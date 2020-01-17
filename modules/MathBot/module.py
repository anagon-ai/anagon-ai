import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

from jsonpickle import Pickler

from core.events import TextInput, TextOutput, BaseEvent
from modules.BaseModule import BaseModule


class Term(ABC):
    @abstractmethod
    def result(self):
        pass


@dataclass
class Constant(Term):
    type = 'constant'
    value: float

    def result(self):
        return self.value


@dataclass
class Addition(Term):
    type = 'addition'
    term1: Term
    term2: Term

    def result(self):
        return self.term1.result() + self.term2.result()


@dataclass
class MathParsed(BaseEvent):
    type = 'be.blannoo.ai.math.parsed'
    expression: Term


class MathBot(BaseModule):

    def boot(self):
        """ Subscribe to relevant events here. """
        self.subscribe(self.handle_text, TextInput)
        self.subscribe(self.execute, MathParsed)
        self.subscribe(self.print_json, MathParsed)

    def handle_text(self, event: TextInput):
        self.publish(MathParsed(expression=self.parser(event.text)))

    def parser(self, text) -> Term:
        if re.match(r'^-?\d+(?:\.\d+)?$', text) is not None:
            return Constant(float(text))
        elif re.match(r'^.*\+.*$', text) is not None:
            term1, term2 = text.split('+', maxsplit=1)
            return Addition(
                term1=self.parser(term1),
                term2=self.parser(term2)
            )

    def execute(self, event: MathParsed):
        self.publish(TextOutput(f'The result is: {event.expression.result()}'))

    def print_json(self, event: MathParsed):
        print(Pickler().flatten(event))
