from patterns.dependency_container import DependencyContainer


def component(cls):
    """
    A decorator for registering a class as a component in the DependencyContainer.

    This decorator adds the provided class to the DependencyContainer. It is then available
    for dependency injection throughout the application.

    :param cls: The class to be registered as a component.
    :return: The same class that was passed in, after it has been registered in the DependencyContainer.

    Note: This decorator is part of a simple dependency injection system. Classes registered with
    this decorator can be automatically injected into other classes using the @autowired decorator.
    """
    DependencyContainer.add_dependency(cls)
    return cls
