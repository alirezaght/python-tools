class AutowiredError(Exception):
    """
    Exception raised when an error occurs in the process of automatic dependency injection.

    This custom exception is used within the context of the dependency injection system,
    particularly with the `@autowired` decorator. It is raised when a required dependency
    cannot be injected.

    Attributes:
        message (str): Explanation of the error.

    Example:
        raise AutowiredError("Dependency 'MyService' not found in DependencyContainer")
    """
    pass
