class ExampleModule(BaseModule):
   def boot(self):
       self.subscribe(self.handle, types=SubscribedEvent)

   def handle(self, event: ExpectedEvent):
       pass