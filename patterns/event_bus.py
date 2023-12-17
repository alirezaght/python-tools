import inspect
from typing import Callable, Hashable, Optional, Any, Dict, List, Type
from threading import Lock

from patterns.event import Event
from patterns.event_error import EventError


class EventBus:
    """
    A class that implements the publish-subscribe pattern for event handling.

    It allows objects to subscribe to specific types of events and get notified
    when such events are posted. The EventBus maintains a registry of subscribers
    and their interested event types.
    """
    subscribers: Dict[
        Hashable, Dict[
            type[Event], List[Callable[..., Any]]]] = {}
    event_bus_lock = Lock()
    observer_funcs = {}

    @classmethod
    def subscribe(cls, instance: Hashable, event: Type[Event],
                  func: Callable[..., Any]):
        """
        Subscribe a callable to an event type.

        :param instance: The instance subscribing to the event. It must be hashable.
        :param event: The type of the event to subscribe to.
        :param func: The callable to invoke when the event is posted.
        :raises EventError: If 'event' is not a subclass of Event.
        """
        if not issubclass(event, Event):
            raise EventError(f"{event} is not a subclass of {Event}")
        with cls.event_bus_lock:
            instance_obj = cls.subscribers.get(instance, None)
            if instance_obj is None:
                cls.subscribers[instance] = {}
            event_arr = cls.subscribers[instance].get(event, None)
            if event_arr is None:
                cls.subscribers[instance][event] = []
            cls.subscribers[instance][event].append(func)

    @classmethod
    def unsubscribe(cls, instance: Hashable,
                    event: Optional[Type[Event]] = None):
        """
        Unsubscribe a callable from an event type.

        :param instance: The instance unsubscribing from the event.
        :param event: The event type to unsubscribe from. If None, unsubscribe from all events.
        :raises EventError: If 'event' is not a subclass of Event.
        """
        with cls.event_bus_lock:
            if instance in cls.subscribers:
                if event is None:
                    cls.subscribers.pop(instance)
                else:
                    if not issubclass(event, Event):
                        raise EventError(
                            f"{event} is not a subclass of {Event}")
                    if event in cls.subscribers.get(instance, {}):
                        cls.subscribers.get(instance, {}).pop(event)

    @classmethod
    def post(cls, event: Event):
        """
        Post an event to notify all subscribed callables.

        :param event: The event instance to post.
        :raises EventError: If 'event' is not an instance of Event.
        """
        if not isinstance(event, Event):
            raise EventError(f"{event} is not an instance of {Event}")
        for instance, items in cls.subscribers.items():
            callables = items.get(type(event))
            if callables is not None and len(callables) > 0:
                for callableFunc in callables:
                    number_of_arguments = len(
                        inspect.signature(callableFunc).parameters)
                    if number_of_arguments == 0:
                        callableFunc()
                        continue
                    elif number_of_arguments == 1:
                        callableFunc(event)
                        continue
                    elif number_of_arguments == 2:
                        callableFunc(instance, event)
                        continue
                    raise EventError(
                        f"{callableFunc} should accept no parameter, or 1 parameter which is the event, or 2 parameter which are self and event inside a class decorated by @observer")


def event_subscribe(event: Type[Event], standalone: bool = False):
    """
    Decorator to subscribe a function or method to an event.

    :param event: The event type to subscribe to.
    :param standalone: If True, the function is subscribed as a standalone function (not bound to a class instance).
    :return: The decorated function.
    """
    def decorator(func):
        if standalone:
            EventBus.subscribe("", event, func)
        else:
            events = EventBus.observer_funcs.get(func, None)
            if events is None:
                EventBus.observer_funcs[func] = set()
            EventBus.observer_funcs[func].add(event)
        return func

    return decorator


def observer(cls: type):
    """
    Class decorator for automatically subscribing methods to events.

    This decorator automatically subscribes all methods in the class that are marked
    with @event_subscribe to their respective events.

    :param cls: The class to be decorated.
    :return: The decorated class.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        for attr_name, attr_value in cls.__dict__.items():
            if inspect.isfunction(attr_value) or inspect.ismethod(attr_value):
                if attr_value in EventBus.observer_funcs:
                    for event in EventBus.observer_funcs[attr_value]:
                        EventBus.subscribe(self, event, attr_value)
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
