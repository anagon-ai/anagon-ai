if __name__ == '__main__':
  ai = Core()

  # add an instance of your module to core
  my_module = ExampleModule()
  ai.add_module(my_module)

  # boot the core instead of the module
  ai.boot()