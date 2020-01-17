import inspect
import logging
from collections import defaultdict
from inspect import isclass
from typing import Callable, Dict, List, Type, Union
from uuid import uuid4

from core.errors import CoreNotBootedError, ModuleError, ModulePublishedBadEventError, \
    ModuleSubscribeEventNotMatchingHandlerError, ModuleSubscribedToNonClassError, ModuleSubscribedToNonEventClassError
from core.events import BaseEvent, All
from core.messaging import Metadata
from core.types import AnyEventHandler, EventMetadataHandler, Types
from modules.BaseModule import BaseModule


class Core:
    modules: List
    handlers: Dict[Union[None, str], List[AnyEventHandler]] = defaultdict(list)
    metadata_provider: Callable[[], Metadata]

    def __init__(self, metadata_provider: Callable[[], Metadata] = lambda: Metadata(id=uuid4())):
        self.modules = []
        self.booted = False
        setattr(self, 'metadata_provider', metadata_provider)

    def add_module(self, module: BaseModule) -> None:
        logging.info("Registering: %s" % type(module).__name__)
        self.modules.append(module)

    def boot(self) -> None:
        for module in self.modules:
            logging.info("Booting module: %s" % type(module).__name__)

            def module_publish(event: BaseEvent, metadata: Metadata = None) -> None:
                return self.publish(event, metadata, module)

            def module_subscribe(handler: AnyEventHandler, types: Types = All) -> None:
                return self._subscribe(module=module, handler=handler, types=types)

            module.attach(publish=module_publish, subscribe=module_subscribe)
            module.boot()

        self.booted = True
        logging.info("Booted all modules")

    def publish(self, event: BaseEvent, metadata: Metadata = None, module: BaseModule = None) -> None:
        if not self.booted:
            raise CoreNotBootedError()

        if not isinstance(event, BaseEvent):
            raise ModulePublishedBadEventError(module=module, event=event)

        metadata = metadata if metadata else self.metadata_provider()

        for handler in self.handlers[event.type] + self.handlers[All.__name__]:
            (handler_args_spec, *_) = inspect.getfullargspec(handler)

            if 'event' in handler_args_spec and 'metadata' in handler_args_spec:
                assert isinstance(handler, EventMetadataHandler)
                handler(event=event, metadata=metadata)
            elif 'event' in handler_args_spec:
                handler(event=event)
            elif 'metadata' in handler_args_spec:
                handler(metadata=metadata)

    def _subscribe(self, module: BaseModule, handler: AnyEventHandler, types: Types = All) -> None:
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
