class PersonDomainException(Exception):
    """
    Exception class for PersonDomain
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ActivityDomainException(Exception):
    """
    Exception class for ActivityDomain
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PersonRepositoryException(Exception):
    """
    Exception class for PersonRepository
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ActivityRepositoryException(Exception):
    """
    Exception class for ActivityRepository
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PersonServiceException(Exception):
    """
    Exception class for PersonService
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ActivityServiceException(Exception):
    """
    Exception class for ActivityService
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UIException(Exception):
    """
    Exception class for UI
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ConditionsException(Exception):
    """
    Exception class for Conditions
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)
