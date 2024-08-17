import os
import typing
from abc import (
    ABC,
    abstractmethod,
)
from lenv.validators import (
    MetadataValidator,
    validate,
)


_TMetadata = typing.TypeVar("_TMetadata", bound=typing.Mapping[str, typing.Any])


class ABCMetadata(ABC):
    @abstractmethod
    def to_dict(self) -> _TMetadata:
        ...


class DefaultMetadata(ABCMetadata):
    @validate(MetadataValidator())
    def to_dict(self) -> _TMetadata:
        return {
            "dotenv_path": ".env"
        }


class ConfigurableMetadata(ABCMetadata):
    def __init__(self, dotenv_path: os.PathLike[str]) -> None:
        self._dotenv_path = dotenv_path

    @validate(MetadataValidator())
    def to_dict(self) -> _TMetadata:
        return {
            "dotenv_path": self._dotenv_path
        }
