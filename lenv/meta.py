# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

import typing as t
import warnings
from os import getenv, PathLike

from dotenv import load_dotenv
from lenv.utils import deserialize


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
    metadata: t.Optional[t.Dict[t.Hashable, t.Any]] = None,
) -> bool:

    if metadata is None:
        metadata = MetaDataUtils.default_metadata()
    MetaDataUtils.implement_required_keys(metadata)

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

            value: t.Optional[t.Any] = None
            if hasattr(heir, key):
                value = getattr(heir, key)

            dotenv_value = getenv(value or key)
            if dotenv_value is None:
                warnings.warn("The key '%s' will return the value 'None', since it is not found in the env variables" % key)

            try:
                dotenv_value = deserialize(
                    value=dotenv_value,
                    type=type_
                )
            except TypeError:
                raise TypeError("Unable to deserialize '{k}' with value '{v}' to type '{t}'".format(
                    k=key,
                    v=dotenv_value,
                    t=type_.__name__
                ))

            setattr(heir, key, dotenv_value)

        return heir
