import inspect

from patterns.autowired_error import AutowiredError


class DependencyContainer:
    """
    A container for managing dependencies used in automatic dependency injection.

    This class serves as a registry for dependencies, allowing classes to be added and
    retrieved based on their types. It is primarily used in conjunction with the
    `@autowired` decorator for injecting dependencies into classes.

    Attributes:
        dependencies (set): A set of registered dependency classes.

    Methods:
        add_dependency: Register a new dependency class.
        get_dependency: Retrieve a registered dependency class based on a given type.

    Example:
        DependencyContainer.add_dependency(MyService)
        service = DependencyContainer.get_dependency(MyService, MyClass)
    """
    dependencies = set()

    @classmethod
    def add_dependency(cls, dependency_cls):
        """
        Registers a new dependency class in the container.

        This method adds the given class to the set of dependencies, making it
        available for automatic injection into classes using the `@autowired` decorator.

        :param dependency_cls: The class to be registered as a dependency.
        """
        cls.dependencies.add(dependency_cls)

    @classmethod
    def get_dependency(cls, dependency_cls, for_cls):
        """
        Retrieves a dependency class based on the given type.

        This method searches through the registered dependencies and finds a class
        that is a subclass of the specified `dependency_cls`. If multiple candidates
        are found, an AutowiredError is raised due to ambiguity.

        :param dependency_cls: The type of the dependency to retrieve.
        :param for_cls: The class for which the dependency is being retrieved.
        :return: The dependency class if found; None otherwise.
        :raises AutowiredError: If multiple candidate dependencies are found.
        """
        candidates = []
        if inspect.isclass(dependency_cls):
            for key in cls.dependencies:
                if inspect.isclass(key) and issubclass(key, dependency_cls):
                    candidates.append(key)
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            raise AutowiredError(f"Warning, Ambiguous references in {for_cls}, {candidates}")
        return None
