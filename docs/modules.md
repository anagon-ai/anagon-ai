# Modules

Anagon AI is built out of independent modules.
You can easily extend the AI by creating your own module.

## Creating a module

1. Generate a template module
   ```bash
   python create_module.py MyAwesomeModule
   ```
2. Edit the module   
   > `modules/MyAwesomeModule/module.py`  
   > Check out some examples below
3. Add your module to `start.py`

   ```python
   ai = Core()
   ai.add_module(MyAwesomeModule())  # add this line
   ai.boot()
   ```
4. Run it!  
   ```bash
   python start.py
   ```
## Module class

Modules consist of a class extending `BaseModule`, with an overwritten `boot()` method:


```python
from modules import BaseModule

class MyAwesomeModule(BaseModule):
    def boot(self):
      ...
```

Within boot, you can **subscribe** to single, multiple or all event types:

```python
      self.subscribe(self.handle_single_event, TextInput)
      
      self.subscribe(self.handle_multiple_events, [TextInput, TextOutput])
      
      self.subscribe(self.handle_all_events)
```

Inside the handlers, you can react to incoming events, for example by **publishing** another [event](events.md):

```python
    def handle_single_event(self, event: TextInput):
      self.publish(TextOutput("I've received an input event!")
    
    def handle_multiple(self, event: Union[TextInput, TextOutput]):
      pass
```

Add the `metadata` argument to access the event's `id` and other [Metadata](metadata.md) 

```python
    def handle_all_events(self, event: BaseEvent, metadata: Metadata):
      pass
```


Methods:

- `def boot(self)` &mdash; method you need to define to initialize your module.
- `def handle[...](event)` &mdash; the module's event handler(s), registered in `boot()`. Defined by you.
  - `async def handle[...](event)` to run the handler asynchronously
- `self.subscribe(handler, types)` &mdash; react to incoming events by subscribing your handlers to specific types.
- `self.publish(event)` &mdash; publish an [Event](events.md) from your module, so other modules can react to it.
- `self.add_task(task)` &mdash; add an asynchronous task, such as a wait-loop

## Examples

> Also check out the included modules in `modules/` to get some inspiration. 


### EventLoggingBot

Simple bot that writes all incoming events to a file:

- notice the usage of `__init__`, `boot` and `handler`

```python
import typing

from core.events import BaseEvent
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

### TimeBot

Bot that prints the time when you say the word `time`, and shows the time _every 60 seconds_.

- notice the usage of `self.publish(TextOutput(...))` to print something to the screen, which is handled by another Module.
- notice the usage of `self.add_task(...)` to run code asynchronously

```python
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
```