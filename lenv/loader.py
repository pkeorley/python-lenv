import inspect
import typing

from dotenv import dotenv_values

from .metadata import (
    DefaultMetadata,
    ABCMetadata,
)
from .config import Config
from .errors import LenvError


def _get_metadata(cls, default: typing.Optional[ABCMetadata] = None) -> typing.Optional[ABCMetadata]:
    """
    Gets the metadata from the class.

    :param cls: Class to get metadata from
    :param default: Default metadata when metadata is not found
    :return: Metadata
    """
    v = getattr(cls, Config.METADATA_CLASS_VAR_NAME, default)
    if isinstance(v, ABCMetadata) is False:
        raise LenvError(f"Value of '%s' variable must be an instance of %s, got %r" % (
            Config.METADATA_CLASS_VAR_NAME, ABCMetadata, type(v)
        ))
    return v


class EnvironmentLoaderMeta(type):
    """
    Metaclass for loading environment variables
    """
    def __new__(cls, name, bases, dct):
        __new_class = type.__new__(cls, name, bases, dct)

        __metadata: ABCMetadata = _get_metadata(__new_class, default=DefaultMetadata())

        __dotenv_values = dotenv_values(__metadata.to_dict()["dotenv_path"])
        for k in inspect.get_annotations(__new_class).keys():
            setattr(__new_class, k, __dotenv_values.get(k))

        return __new_class


class EnvironmentLoader(metaclass=EnvironmentLoaderMeta):
    """
    Class for loading environment variables
    """
    pass
