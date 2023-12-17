from patterns.dependency_container import DependencyContainer


class Prototype(type):
    """
    A metaclass for creating prototype instances.

    This metaclass overrides the default __call__ method to ensure that a new instance
    is created each time a class with this metaclass is instantiated. It is used to
    implement the Prototype design pattern, where each instance created from a class
    is unique and not shared.

    The Prototype metaclass uses the standard __call__ method of 'type' to create a new
    instance of the class and then returns this instance.

    Usage:
        class MyClass(metaclass=Prototype):
            pass

        # Each time MyClass is instantiated, a new, unique instance is created.
        instance1 = MyClass()
        instance2 = MyClass()
        assert instance1 is not instance2
    """
    def __call__(cls, *args, **kwargs):
        instance = super(Prototype, cls).__call__(*args,
                                                  **kwargs)
        return instance


def prototype(cls: type):
    """
    A decorator for registering a class as a prototype in the DependencyContainer.

    When this decorator is applied to a class, it modifies the class's __new__ method
    to ensure that a new instance of the class is created each time it is instantiated.
    The class is also registered in the DependencyContainer, making it available for
    dependency injection as a prototype.

    Args:
        cls (type): The class to be treated as a prototype and registered.

    Returns:
        type: The same class with its __new__ method modified to enforce prototype behavior.

    Usage:
        @prototype
        class MyPrototypeClass:
            pass

        # Each instantiation of MyPrototypeClass results in a new instance.
        instance1 = MyPrototypeClass()
        instance2 = MyPrototypeClass()
        assert instance1 is not instance2
    """
    DependencyContainer.add_dependency(cls)
    original_new = cls.__new__

    def new_prototype(cls):
        return original_new(cls)

    cls.__new__ = new_prototype
    return cls
