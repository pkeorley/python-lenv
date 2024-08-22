import os
import typing
from abc import (
    ABC,
    abstractmethod,
)
from .validators import (
    MetadataValidator,
    validate,
)


TMetadata = typing.TypeVar("TMetadata", bound=typing.Mapping[str, typing.Any])


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


class DefaultMetadata(ABCMetadata):
    """
    A default implementation of the Metadata class where configuration options are disabled.

    This class serves as a fallback or default metadata implementation when no specific metadata is
    provided. It includes minimal configuration with fixed values that cannot be altered.
    """

    @validate(MetadataValidator())
    def to_dict(self) -> TMetadata:
        """
        Converts the default metadata into a dictionary format.

        :return: A dictionary representation of the metadata
        """
        return {
            "dotenv_path": ".env"
        }


class ConfigurableMetadata(ABCMetadata):
    """
    Represents the configurable metadata. Configuration is enabled.
    """
    def __init__(self, dotenv_path: os.PathLike[str]) -> None:
        self._dotenv_path = dotenv_path

    @validate(MetadataValidator())
    def to_dict(self) -> TMetadata:
        """
        Converts the default metadata into a dictionary format.

        :return: A dictionary representation of the metadata
        """
        return {
            "dotenv_path": self._dotenv_path
        }
