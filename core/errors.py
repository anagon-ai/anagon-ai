from typing import Callable

from util.developer_help import message_with_example


class CoreError(Exception):
  pass


class ModuleError(Exception):
  pass


class CoreNotBootedError(CoreError):

  def __init__(self) -> None:
    super().__init__(message_with_example(
      message="AI has not been booted yet. Please run Core.boot() before publishing.",
      example='docs/examples/boot_core.py'
    ))


class ModulePublishedBadEventError(ModuleError):

  def __init__(self, module, event) -> None:
    super().__init__(message_with_example(
      message=
      """ExampleModule is publishing an event of type `%(type)s` instead an instance of `BaseEvent`.

For a list of event types you can publish, see:
  - https://github.com/anagon-ai/anagon-ai/blob/master/docs/events.md
""" % {
        'type': type(event).__name__
      },
      example='docs/examples/module_publish_event.py',
      object=module,
      params={
        'ExampleModule': module.__class__.__name__
      }
    ))


class ModuleSubscribedToNonClassError(ModuleError):

  def __init__(self, module, event) -> None:
    super().__init__(message_with_example(
      message=
      """ExampleModule is subscribing to an event of type `%(type)s` instead of a child-class of `BaseEvent`.

For a list of event types you can subscribe to, see:
  - https://github.com/anagon-ai/anagon-ai/blob/master/docs/events.md
""" % {
        'type': type(event).__name__
      },
      example='docs/examples/module_subscribe_event_not_class.py',
      object=module,
      params={
        'ExampleModule': module.__class__.__name__,
        'TextInput': '\033[4;38;5;82m%s\033[0m' % 'TextInput',
        '\'EventAsString\'': '\033[4;38;5;196m%s\033[0m' % repr(event)
      }
    ))


class ModuleSubscribedToNonEventClassError(ModuleError):

  def __init__(self, module, event) -> None:
    super().__init__(message_with_example(
      message=
      "ExampleEvent is not a valid event, because it does not extend `BaseEvent`." % {
        'type': type(event).__name__
      },
      example='docs/examples/module_subscribe_event_not_event_class.py',
      object=event,
      params={
        'ExampleModule': module.__class__.__name__,
        'ExampleEvent': event.__name__,
        'BaseEvent': '\033[1;31;4mBaseEvent\033[0m'
      }
    ))

def bad(text):
  return '\033[1;31;4m%s\033[0m' % text

def good(text):
  return '%s' % text

class ModuleSubscribeEventNotMatchingHandlerError(ModuleError):

  def __init__(self, module, handler: Callable, event) -> None:
    super().__init__(message_with_example(
      message=
      "ExampleModule subscribes to SubscribedEvent,\n  but its ModuleWithTypeMismatch.ExampleHandler() expects a type ExpectedEvent .",
      example='docs/examples/module_subscribe_event_not_matching_handler.py',
      # object=handler,
      params={
          'ExampleModule': module.__class__.__name__,
          'SubscribedEvent': bad(event.__name__),
          'ExpectedEvent': bad(handler.__annotations__['event'].__name__),
          'ExampleHandler': handler.__name__,
          }
      ))


class ModulePublishedBeforeAttachingError(ModuleError):

  def __init__(self, module) -> None:
    super().__init__(message_with_example(
      example="docs/examples/append_module.py",
      message="""
%(class)s was not attached to Core before publishing.

You cannot boot your module directly (like: %(class)s.boot()).
It must instead be added to the AI Core, which is boots the modules for you. 
        """ % {'class': module.__class__.__name__}
      ))


class ModuleSubscribedBeforeAttachingError(ModuleError):
  def __init__(self, module) -> None:
    super().__init__(message_with_example(
      example="docs/examples/append_module.py",
      message="""
%(class)s was not attached to Core before subscribing.

You cannot boot your module directly (like: %(class)s.boot()).
It must instead be added to the AI Core, which is boots the modules for you. 
""" % {'class': module.__class__.__name__}
      ))


class ModuleAddedTaskBeforeAttachingError(ModuleError):
  def __init__(self, module) -> None:
    super().__init__(message_with_example(
      example="docs/examples/append_module.py",
      message="""
%(class)s was not attached to Core before adding task.

You cannot boot your module directly (like: %(class)s.boot()).
It must instead be added to the AI Core, which is boots the modules for you. 
""" % {'class': module.__class__.__name__}
      ))
