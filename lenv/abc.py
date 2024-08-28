from abc import (
    ABC,
    abstractmethod
)

from .types import TMetadata


class ABCThrowable(ABC):
    @abstractmethod
    def throw(self) -> BaseException:
        """
        Helps to handle the exception in a generic way

        :return: An instance based on the `BaseException` class
        """
        ...


class ABCMetadata(ABC):
    """
    Represents the abstract base class for metadata.
    """

    @abstractmethod
    def to_dict(self) -> TMetadata:
        """
        Converts the default metadata into a dictionary format.

        :return: A dictionary representation of the metadata
        """
        ...


class ABCValidator(ABCThrowable, ABC):
    """
    Abstract base class for validating data
    """
    @abstractmethod
    def is_valid(self, obj: object) -> bool:
        """
        Validates whether the provided object meets the metadata requirements.

        :param obj: Object to validate
        :return: Boolean indicating whether the object is valid
        """
        ...
