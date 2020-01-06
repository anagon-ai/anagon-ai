class ExampleClass(BaseModule):

  # add this method
  def boot(self):
    self.subscribe(self.handler)

  def handler(self, event: BaseEvent):
    pass