import collections
import inspect
import typing

from dotenv import dotenv_values

from .metadata import (
    DefaultMetadata,
    ABCMetadata,
)
from .config import Config


def _get_metadata(cls, default: typing.Optional[ABCMetadata] = None) -> typing.Optional[ABCMetadata]:
    v = getattr(cls, Config.METADATA_CLASS_VAR_NAME, default)
    if isinstance(v, ABCMetadata) is False:
        raise ValueError(f"Value of '%s' variable must be an instance of %s, got %r" % (
            Config.METADATA_CLASS_VAR_NAME, ABCMetadata, type(v)
        ))
    return v


class EnvironmentLoaderMeta(type):
    def __new__(cls, name, bases, dct):
        __new_class = type.__new__(cls, name, bases, dct)

        __metadata: ABCMetadata = _get_metadata(__new_class, default=DefaultMetadata())
        __dotenv_values = dotenv_values(__metadata.to_dict()["dotenv_path"])

        __annotations = inspect.get_annotations(__new_class)

        for k, _ in __annotations.items():
            setattr(__new_class, k, __dotenv_values.get(k))

        return __new_class


class EnvironmentLoader(metaclass=EnvironmentLoaderMeta):
    pass
