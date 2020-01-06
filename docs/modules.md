# Modules

Anagon AI is built out of independent modules.
You can easily extend the AI by creating your own module.

To do this:

- create a folder with your module name inside `modules`, with a file called `module.py` in it.
  e.g.: `modules/GreetingBot/module.py`
- in `module.py`, create a class that extends `BaseModule`  
  
  Here's an example of a simple Bot that shows different greetings each time the user typed 'hello'.
  
  ```python
  from modules.BaseModule import BaseModule
  from events import TextInput
  from events import TextOutput
  
  class GreetingBot(BaseModule):
    greetings: list  
    greetingIndex: int
  
    def boot(self):
      self.greetings = [
        'hello there',
        'what\'s up!',
        'heya!'
      ] 
      self.greetingIndex = 0
      self.subscribe(self.handle, types=TextInput.type)
                
    def handle(self, message: TextInput):
      if message.text.find("hello") > -1:
        greetings = self.greetings[self.greetingIndex]
        self.greetingIndex = (self.greetingIndex + 1) % len(self.greetings)
        self.publish(TextOutput(greetings))
        
  ```
- Load your module within start.py

  ```python
  
  ai = Core()
  ai.add_module(GreetingBot())
  ai.add_module(TextInputModule())

  ai.boot()
  ```
- Run start.py  
  `python start.py`
## Module class

Modules consist of a class extending BaseModule, with an overwritten boot method.

Within boot, you can subscribe to single, multiple or all event types.

Methods:

- `def boot()` &mdash; method you need to define to initialize your module.
- `def handle[...](event)` &mdash; the module's event handler(s), registered in `boot()`. Defined by you.
- `self.subscribe(handler, types)` &mdash; react to incoming events by subscribing your handlers to specific types.
- `self.publish(event)` &mdash; publish an [Event](events.md) from your module, so other modules can react to it.

### Example
 
Simple bot that writes all incoming events to a file.

```python
import typing

from events import BaseEvent
from modules.BaseModule import BaseModule


class EventLoggingBot(BaseModule):
  file: typing.TextIO = None

  def __init__(self, log_location: str):
    self.log_location = log_location

  def boot(self):
    self.file = open(self.log_location, 'a')
    self.subscribe(self.handler)

  def handler(self, event: BaseEvent):
    self.file.write("Event received: %s\n" % (event,))
    self.file.flush()
```

See above how to add the module to the AI.