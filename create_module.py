import argparse
import os
import pathlib
import sys

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Create a new module.', usage="\n  python create_module.py NAME\n\nexample:\n  python create_module.py MyAwesomeModule\n")
  parser.add_argument('name', type=str, help='Module name. Example: MyAwesomeModule')
  args = parser.parse_args()

  module_name = args.name

  base_dir = os.path.realpath(os.path.dirname(__file__))
  module_dir = '%s/modules/%s' % (base_dir, module_name)
  module_path = '%s/module.py' % (module_dir,)

  template_dir = '%s/modules/__template__' % (base_dir,)
  template_path = '%s/module.py' % (template_dir,)

  print('Creating module', module_name)
  with open(template_path, 'r') as template_file:
    pathlib.Path(module_dir).mkdir(parents=True, exist_ok=True)
    try:
      with open(module_path, 'x') as module_file:
        module_file.write(template_file.read().replace('TemplateModule', module_name))
        open('%s/__init__.py' % module_dir, 'a').close()
    except FileExistsError:
      print('Error: Module already exists or directory not empty', file=sys.stderr)

  print('Done.')
  print('file://%s' % module_path)
