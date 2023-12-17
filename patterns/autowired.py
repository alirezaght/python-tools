from typing import get_type_hints

from patterns.dependency_container import DependencyContainer


def autowired(cls: type):
    """
    A decorator for enabling automatic dependency injection in a class.

    This decorator modifies the `__init__` method of the class to automatically
    inject dependencies. It relies on the type annotations of the class attributes
    to determine which dependencies to inject. Each annotated attribute is
    expected to correspond to a key in the DependencyContainer. The decorator
    retrieves each dependency from the container and assigns it to the respective
    attribute of the class instance.

    Usage of this decorator implies that the required dependencies have already been
    registered in the DependencyContainer.

    :param cls: The class to be decorated for dependency injection.
    :return: The same class, modified to have automatic dependency injection in its `__init__` method.

    Example:
        @autowired
        class MyClass:
            my_service: MyService  # MyService should be registered in the DependencyContainer

            def my_method(self):
                return self.my_service.do_something()
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        for key, t in cls.__annotations__.items():
            dependency = DependencyContainer.get_dependency(t, cls)
            if dependency:
                setattr(self, key,
                        dependency() if callable(dependency) else dependency)
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
