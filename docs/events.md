# Events


## Creating Events

In your `module.py` file, create a class that extends [BaseEvent](../core/events.py).


```python
from dataclasses import dataclass
from core.events import BaseEvent
from datetime import date, time

@dataclass
class ExampleCalendarEvent(BaseEvent):
  type = 'com.mywebsite.anagon.ai.calendar.event.started'
  title: str
  start_date: date
  start_time: time
  end_date: date
  end_time: time
```

## Publishing Events

> todo 

## Core Events

### TextInput

User has typed some text into the console.
Provided by [ConsoleModule](../modules/ConsoleModule/module.py).

- type = `be.anagon.ai.poc.text.input`
- text: str &mdash; content of the input


### TextOutput

Publish this event to print text to the console.
Handled by [ConsoleModule](../modules/ConsoleModule/module.py).

- type = `be.anagon.ai.poc.text.output`
- text: str &mdash; content to be printed