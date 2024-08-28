import typing


# Type var that represents metadata (a dict)
TMetadata = typing.TypeVar("TMetadata", bound=typing.Mapping[str, typing.Any])
