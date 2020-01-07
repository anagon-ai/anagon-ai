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
