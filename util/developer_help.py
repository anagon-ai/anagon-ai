import inspect
import os

from util import source_printer, colors


def message_with_example(message, example, params={}, object=None):
  try:
    with open(os.path.dirname(__file__) + '/../' + example) as source_file:
      source = source_file.read()
      source_pretty = source_printer.render(source, default_color=colors.syntax.default)
  except Exception as e:
    print(e)
    source_pretty = '(could not load source: %s)' % e
  output = '\n\033[97m' + message + '\n\n\033[0mExample:\033[0m\n\n' + '\n'.join(
    ['   ' + l for l in source_pretty.splitlines()])
  for k in params:
    output = output.replace(k, params[k])

  if object:
    object_class = object if inspect.isclass(object) else object.__class__
    lines, line_no = inspect.getsourcelines(object_class)
    output += '\n\nSee: \033[94mfile://%s:%s\033[0m' % (inspect.getfile(object_class), line_no)

  return output
