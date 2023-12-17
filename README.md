# Python Tools

## Overview
Python Tools is a comprehensive collection of design patterns for Python development. This repository includes various implementations of design patterns and their corresponding test cases, focusing on enhancing the flexibility and robustness of Python applications.

## Features
- **Design Patterns**: 
  - `singleton.py`: Implementation of the Singleton pattern.
  - `prototype.py`: Implementation of the Prototype pattern.
  - `component.py`: Base component class for pattern implementations.
  - `event.py`: Base class for event handling.
  - `event_bus.py`: Implementation of the EventBus pattern for event-driven architectures.
  - `dependency_container.py`: Implementation of a dependency container, facilitating dependency injection.
  - `autowired.py`: Decorator for autowiring dependencies in classes.
  - `event_error.py`, `autowired_error.py`: Custom exception classes for event and autowiring related errors.

- **Testing**:
  - `singleton_test.py`: Test cases for the Singleton pattern.
  - `event_bus_test.py`: Test cases for the EventBus pattern.
  - `autowired_test.py`: Test cases for the Autowired functionality.

## Getting Started
To use these tools in your project, clone the repository and import the necessary modules:

```bash
git clone https://github.com/alirezaght/python-tools.git
```

## Usage

Each module in the `patterns` directory can be imported and used in your Python projects. Here's an example of how to use the Singleton pattern:

```python
from patterns.singleton import Singleton, singleton

class MySingletonClass(metaclass=Singleton):
    pass

@singleton
class MySingletonClassUsingDecorator:
    pass
```

## Autowiring Use Case
The `autowired` module in this repository provides a powerful way to manage dependencies in your Python applications. It simplifies the process of injecting dependencies into your classes, reducing the need for manual instantiation and making your codebase more modular and testable.

### How to Use Autowiring
To use autowiring, you need to define your dependencies and decorate your class or method with the `@autowired` decorator. This automatically injects the required dependencies when an instance of the class is created.

Here's a simple example:

```python
from patterns.autowired import autowired
from patterns.component import component

# Assuming you have a dependency class it should be decorated with one of @component, @singleton or @prototype decorators
@component
class SomeDependency:
    def perform_task(self):
        print("Task performed.")

# Using autowired in your class
@autowired
class MyClass:
    some_dependency: SomeDependency
    
    def use_dependency(self):
        self.some_dependency.perform_task()

# Creating an instance of MyClass will automatically inject SomeDependency
my_class_instance = MyClass()
my_class_instance.use_dependency()  # Output: "Task performed."

```

In this example, MyClass requires an instance of SomeDependency. By using the @autowired decorator, SomeDependency is automatically injected when MyClass is instantiated, thus decoupling the creation of dependencies from the class itself.

### Benefits of Autowiring
- **Reduced Boilerplate**: Automatically injects dependencies, reducing the amount of setup code.
- **Improved Modularity**: Encourages a modular design by separating the instantiation of dependencies from their usage.
- **Enhanced Testability**: Makes unit testing easier as dependencies can be easily mocked or replaced.
- **Increased Flexibility**: Easily swap out implementations of dependencies without changing the dependent classes.


## EventBus Use Case
The `event_bus` module provides an implementation of the EventBus pattern, which is a powerful way to enable event-driven architecture in your Python applications. It allows for decoupling components that emit events from components that process events, facilitating a more modular and extensible design.

### How to Use EventBus
EventBus allows objects to subscribe to specific types of events and get notified when such events are posted. Here's a basic example of how to use the EventBus:

```python
from patterns.event_bus import EventBus, event_subscribe, observer
from patterns.event import Event

# Define an event class
class MyEvent(Event):
    pass

# Subscriber function
@event_subscribe(MyEvent, standalone=True)
def handle_my_event(event):
    print("Received MyEvent")

@observer
class ObserverClass:
    
    @event_subscribe(MyEvent)
    def handle_my_event(self, event):
        print("Received MyEvent")
    
    
# Post an event
EventBus.post(MyEvent())
```
In this example:

- `MyEvent` is a subclass of `Event`.
- `handle_my_event` is a function that handles events of type `MyEvent`.
- The function is subscribed to `MyEvent` using `@event_subscribe` decorator.
- If the function is inside a class the class should have `@observer` decorator otherwise in `@event_subscribe`, `standalone` should be True
- When `MyEvent` is posted using `EventBus.post`, `handle_my_event` is automatically called.

### Benefits of EventBus
- **Loose Coupling**: Producers of events do not need to know about the consumers, reducing dependencies between components.
- **Improved Code Organization**: Event handling logic can be separated from the main business logic.
- **Scalability and Flexibility**: New event types and handlers can be easily added without modifying existing code.
- **Asynchronous Processing**: Events can be processed asynchronously, which is useful for tasks that do not require immediate action or response.


## Contributing

Contributions to Python Tools are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-sourced under the MIT License.