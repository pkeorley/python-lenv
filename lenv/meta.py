# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

import typing as t
from os import getenv, PathLike

from dotenv import load_dotenv


class MetaDataUtils:
    @staticmethod
    def default_metadata() -> t.Dict[t.Hashable, t.Any]:
        return MetaDataUtils.implement_required_keys({})

    @staticmethod
    def implement_required_keys(d: t.Dict[t.Hashable, t.Any]) -> t.Dict[t.Hashable, t.Any]:
        if "load_dotenv" not in d:
            d["load_dotenv"] = {}
        return d


def _load_dotenv(
    dotenv_path: t.Optional[t.Union[str, 'PathLike[str]']] = None,
    stream: t.Optional[t.IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: t.Optional[str] = "utf-8",
    metadata: t.Dict[t.Hashable, t.Any] = None,
) -> bool:

    if metadata is None:
        metadata = MetaDataUtils.default_metadata()

    metadata_load_dotenv = metadata["load_dotenv"]
    return load_dotenv(
        dotenv_path=metadata_load_dotenv.get("dotenv_path", dotenv_path),
        stream=metadata_load_dotenv.get("stream", stream),
        verbose=metadata_load_dotenv.get("verbose", verbose),
        override=metadata_load_dotenv.get("override", override),
        interpolate=metadata_load_dotenv.get("interpolate", interpolate),
        encoding=metadata_load_dotenv.get("encoding", encoding),
    )


class Meta(type):
    def __new__(cls, name, bases, dct):
        heir = super().__new__(cls, name, bases, dct)

        metadata: t.Optional[t.Dict[t.Hashable, t.Any]] = None
        if hasattr(heir, "metadata"):
            metadata = getattr(heir, "metadata")
        _load_dotenv(metadata=metadata)

        for key, type_ in heir.__annotations__.items():
            value = None

            if hasattr(heir, key) and getattr(heir, key) is not None:
                value = getattr(heir, key)

            key = value or key

            dotenv_value = getenv(key)

            try:
                dotenv_value = type_(dotenv_value)
            except Exception:
                raise ValueError(f"Failed to convert the environment variable '{key}' "
                                 f"with value '{dotenv_value}' to type '{type_.__name__}'")

            setattr(heir, key, dotenv_value)

        return heir
