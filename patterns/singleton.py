from patterns.dependency_container import DependencyContainer


class Singleton(type):
    """
    A metaclass for implementing the Singleton design pattern.

    This metaclass ensures that only one instance of any class using this metaclass
    is created. If an instance of the class already exists, the existing instance is
    returned instead of creating a new one. The instances are stored in a class-level
    dictionary 'instances'.

    Usage:
        class MyClass(metaclass=Singleton):
            pass

        # Only one instance of MyClass is created, regardless of the number of times it is instantiated.
        instance1 = MyClass()
        instance2 = MyClass()
        assert instance1 is instance2  # This will be True
    """
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args,
                                                                **kwargs)
        return cls.instances[cls]


def singleton(cls: type):
    """
    A decorator for registering a class as a singleton in the DependencyContainer.

    This decorator modifies the class's __new__ method to implement the Singleton
    pattern, ensuring that only one instance of the class exists. When applied, it
    automatically registers the class in the DependencyContainer. The single instance
    of the class is created and returned upon the first instantiation, and subsequent
    instantiations return the same instance.

    Args:
        cls (type): The class to be treated as a singleton and registered.

    Returns:
        type: The same class, modified to enforce singleton behavior.

    Usage:
        @singleton
        class MySingletonClass:
            pass

        # Only one instance of MySingletonClass is created.
        instance1 = MySingletonClass()
        instance2 = MySingletonClass()
        assert instance1 is instance2  # This will be True
    """
    DependencyContainer.add_dependency(cls)
    original_new = cls.__new__

    def new_singleton(cls):
        if cls not in Singleton.instances:
            Singleton.instances[cls] = original_new(cls)
        return Singleton.instances[cls]

    cls.__new__ = new_singleton
    return cls
