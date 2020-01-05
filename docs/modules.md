# Modules

The Anagon AI is built out of independent modules.
You can easily extend the AI by creating your own module.

To do this:

- create a folder with your module name inside `modules`, with a file called `module.py` in it.
  e.g.: `modules/DiscordConnector/module.py`
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
                
    def handle(self, message: TextInput):
      if message.text.find("hello") > -1:
        greetings = self.greetings[self.greetingIndex]
        self.greetingIndex = (self.greetingIndex + 1) % len(self.greetings)
        self.core.publish(TextOutput(greetings))
        
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

The module classes have two methods that you may override:

- `boot(self, core: Core)`
- `handle(self, message)`

Variables available in every module:

- `self.core`: Reference to Core AI module. Use `self.core.publish(event)` to publish an event to other modules

### boot
 
Overriding optional. Used to initialize your module. For example, you can start never-ending threads here, or load data from a file, load some statistical model, etcetera.

### handle

Override to handle incoming events. For example, you can react to TextInput events, or UserHome event, if some other module emits those type of events. You can look at available events [here](./events.md)