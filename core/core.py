import asyncio
import inspect
import logging
import sys
from asyncio import Task
from asyncio.events import AbstractEventLoop
from collections import defaultdict
from inspect import isclass
from typing import Callable, Coroutine, Dict, List, Optional, Type, Union
from uuid import uuid4

from core.errors import CoreNotBootedError, ModuleError, ModulePublishedBadEventError, \
    ModuleSubscribeEventNotMatchingHandlerError, ModuleSubscribedToNonClassError, ModuleSubscribedToNonEventClassError, \
    ModuleSubscribedAfterBoot
from core.events import All, BaseEvent, ExitCommand
from core.messaging import Metadata
from core.types import AnyEventHandler, EventHandler, EventMetadataHandler, EventTypes, MetadataHandler, \
    NoArgumentHandler
from modules.BaseModule import BaseModule

class CoreModule(BaseModule):
    def boot(self) -> None:
        self.subscribe(self.on_exit, ExitCommand)

    async def on_exit(self) -> None:
        await asyncio.sleep(3)
        print("Exit")
        sys.exit()

class Core:
    modules: List
    handlers: Dict[Union[None, str], List[AnyEventHandler]] = defaultdict(list)
    metadata_provider: Callable[[], Metadata]
    tasks: List[Union[Coroutine, Task]]
    loop: AbstractEventLoop

    def __init__(self, metadata_provider: Callable[[], Metadata] = lambda: Metadata(id=uuid4())):
        self.tasks = []
        self.modules = [CoreModule()]
        self.booted = False
        setattr(self, 'metadata_provider', metadata_provider)

    def add_module(self, module: BaseModule) -> None:
        logging.info("Registering: %s" % type(module).__name__)
        self.modules.append(module)

    async def boot_module(self, module: BaseModule) -> None:
        logging.info("Booting module: %s" % type(module).__name__)

        def module_publish(event: BaseEvent, metadata: Metadata = None) -> None:
            return self.publish(event, metadata, module)

        def module_subscribe(handler: AnyEventHandler, types: EventTypes = All) -> None:
            return self._subscribe(module=module, handler=handler, types=types)

        def module_add_task(task: Coroutine) -> None:
            logging.info(f"Added task: {type(module).__name__}.{task.__name__}")
            self.add_task(task)

        module.attach(publish=module_publish, subscribe=module_subscribe, add_task=module_add_task)
        module.boot()

        def raise_exception(handler: AnyEventHandler = None, types: EventTypes = All) -> None:
            raise ModuleSubscribedAfterBoot(module=module)

        module.attach(subscribe=raise_exception)

    def boot(self) -> None:
        self.loop = asyncio.get_event_loop()

        # boot modules and gather tasks
        module_boot_tasks = [self.boot_module(module) for module in self.modules]
        self.loop.run_until_complete(asyncio.gather(*module_boot_tasks))
        logging.info("Booted all modules")
        self.booted = True

        # running module tasks
        logging.info(f"Running module tasks")
        while self.tasks:
            new_tasks, self.tasks = self.tasks[:], []
            self.loop.run_until_complete(asyncio.gather(*new_tasks))

    def publish(self, event: BaseEvent, metadata: Metadata = None, module: BaseModule = None) -> None:
        if not self.booted:
            raise CoreNotBootedError()

        if not isinstance(event, BaseEvent):
            raise ModulePublishedBadEventError(module=module, event=event)

        _metadata: Metadata = metadata if metadata else self.metadata_provider()

        for handler in self.handlers[event.type] + self.handlers[All.__name__]:
            (handler_args_spec, *_) = inspect.getfullargspec(handler)

            def exec_handler() -> Optional[Coroutine]:
                if 'event' in handler_args_spec and 'metadata' in handler_args_spec:
                    assert isinstance(handler, EventMetadataHandler)
                    return handler(event=event, metadata=_metadata)
                elif 'event' in handler_args_spec:
                    assert isinstance(handler, EventHandler)
                    return handler(event=event)
                elif 'metadata' in handler_args_spec:
                    assert isinstance(handler, MetadataHandler)
                    return handler(metadata=_metadata)
                elif len(set(handler_args_spec).difference({'self'})) == 0:
                    assert isinstance(handler, NoArgumentHandler)
                    return handler()
                else:
                    raise ModuleError(f'Invalid handler: {handler_args_spec}')

            handler_return_value = exec_handler()

            # Support co-routines
            if isinstance(handler_return_value, Coroutine):
                self.add_task(handler_return_value)
            elif handler_return_value is not None:
                raise ModuleError('Module handler should not return any value')

    def add_task(self, coroutine: Coroutine) -> None:
        if not self.booted:
            self.tasks.append(coroutine)
        else:
            task = self.loop.create_task(coroutine)
            self.tasks.append(task)

    def _subscribe(self, module: BaseModule, handler: AnyEventHandler, types: EventTypes = All) -> None:
        """Internal: Attaches a module's event handler to all types or a specific set of types"""

        # todo: permission check
        if module:
            pass

        (handler_args_spec, *_) = inspect.getfullargspec(handler)
        valid_arguments = {'self', 'event', 'metadata'}
        invalid_arguments = set(handler_args_spec).difference(valid_arguments)
        if invalid_arguments:
            raise ModuleError(
                "Module '%s' subscribes a handler '%s' with invalid arguments: %s" % (
                        type(module).__name__, handler.__name__, repr(invalid_arguments)[1:-1]))

        # noinspection Mypy
        types_list: List[Type[BaseEvent]] = types if type(types) == list else [types]

        for _type in types_list:
            if _type is All:
                self.handlers[All.__name__].append(handler)
            elif isclass(_type):
                if issubclass(_type, BaseEvent):
                    event_annotation = handler.__annotations__['event'] if 'event' in handler.__annotations__ else None
                    if isclass(event_annotation) and event_annotation != _type:
                        raise ModuleSubscribeEventNotMatchingHandlerError(
                            module=module,
                            handler=handler,
                            event=_type
                            )

                    self.handlers[str(_type.type)].append(handler)
                else:
                    raise ModuleSubscribedToNonEventClassError(event=_type, module=module)
            elif _type is not None:
                raise ModuleSubscribedToNonClassError(event=_type, module=module)
