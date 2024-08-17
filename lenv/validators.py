import functools
import typing
from abc import (
    ABC,
    abstractmethod
)


class ABCValidator(ABC):
    @abstractmethod
    def is_valid(self, obj: object) -> bool:
        ...

    @abstractmethod
    def throw(self) -> BaseException:
        ...


class MetadataValidator(ABCValidator):
    def __init__(self):
        """
        Initializes an instance of MetadataValidator.

        This constructor initializes the `_throw_msg` attribute to `None`. This attribute
        is used to store error messages that will be raised if the validation fails.
        """
        self._throw_msg: typing.Optional[str] = None

    def is_valid(self, obj: object) -> bool:
        """
        Validates whether the provided object meets the metadata requirements.

        This method checks if the given object is an instance of `typing.Mapping`.
        If not, it raises an error. The method then checks for the presence of
        specific keys in the object, such as `"dotenv_path"`. If any required key
        is missing, a `RuntimeError` is raised.

        :param obj:
            The object to validate. Expected to be a `typing.Mapping` instance that
            represents metadata configuration.
        :return:
            `True` if the object is valid and contains all required keys.
        :raises RuntimeError:
            If the object is not a `typing.Mapping` or if any required key is missing.
        """
        if not isinstance(obj, typing.Mapping):
            self._throw("Object is not an instance of 'typing.Mapping'")

        # obj: '_TMetadata'

        # TODO: Better this validation
        for k in ["dotenv_path"]:
            if k not in obj.keys():
                raise RuntimeError(f"Key '%s' should exist in the metadata configuration" % k)

        return True

    def _throw(self, msg: str):
        """
        Stores an error message and raises a RuntimeError.

        This method sets the `_throw_msg` attribute to the provided message and
        then calls the `throw` method to raise the exception.

        :param msg:
            The error message to be stored and raised.
        """
        self._throw_msg = msg
        self.throw()

    def throw(self) -> BaseException:
        """
        Raises a RuntimeError with the stored error message.

        This method raises a `RuntimeError` using the message stored in `_throw_msg`.

        :return:
            Raises `RuntimeError`.
        :raises RuntimeError:
            When called, this method raises an exception with the stored `_throw_msg`.
        """
        raise RuntimeError(self._throw_msg)


def validate(validator: ABCValidator):
    def decorator(func: typing.Callable):
        """
        This function should be used as decorator.
        The main point is validating an output of function using specified validator
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)

            if validator.is_valid(res) is False:
                raise validator.throw()

            return res

        return wrapper

    return decorator
