# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

import re
import typing as t
import warnings
from os import getenv, PathLike

from dotenv import load_dotenv

from lenv.metadata import Metadata, Dict
from lenv.utils import (
    deserialize,
    _getattr
)


def _load_dotenv(
    metadata: t.Union[Metadata, t.Dict[t.Hashable, t.Any]],
    dotenv_path: t.Optional[t.Union[str, 'PathLike[str]']] = None,
    stream: t.Optional[t.IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: t.Optional[str] = "utf-8",
) -> bool:
    """
    Loads environment variables from a dotenv file. Need to specify `metadata` to load the dotenv file.
    :param metadata: Metadata
    :param dotenv_path: Path to the dotenv file
    :param stream: File-like object
    :param verbose: Print out debug info
    :param override: Override existing environment variables
    :param interpolate: Interpolate environment variables
    :param encoding: File encoding
    :return: True if the dotenv file was loaded successfully
    """
    metadata = Metadata(metadata) if isinstance(metadata, dict) else metadata

    return load_dotenv(
        dotenv_path=metadata["load_dotenv"].get("dotenv_path", dotenv_path),
        stream=metadata["load_dotenv"].get("stream", stream),
        verbose=metadata["load_dotenv"].get("verbose", verbose),
        override=metadata["load_dotenv"].get("override", override),
        interpolate=metadata["load_dotenv"].get("interpolate", interpolate),
        encoding=metadata["load_dotenv"].get("encoding", encoding),
    )


class MetaEnvironmentVariablesLoader(type):
    def __new__(cls, name, bases, dct):
        heir = super().__new__(cls, name, bases, dct)

        metadata: t.Optional[Dict] = _getattr(heir, "metadata")

        if metadata is None:
            metadata = Metadata.default()
        else:
            metadata = Metadata.add_required_keys(metadata)

        _load_dotenv(metadata=metadata)

        for key, type_ in heir.__annotations__.items():

            def check(k: str) -> bool:
                """
                Check if the key should be loaded
                :return: True if the key should be loaded, False otherwise
                """
                includes = [re.compile(s) for s in metadata["filters"].get("includes", [])]
                excludes = [re.compile(s) for s in metadata["filters"].get("excludes", [])]

                if includes and not any(i.match(k) for i in includes):
                    return False
                if excludes and any(e.match(k) for e in excludes):
                    return False
                return True

            value: t.Optional[t.Any] = _getattr(heir, key)

            if not check(value or key):
                setattr(heir, key, None)
                continue

            dotenv_value = getenv(value or key)
            if dotenv_value is None:

                if metadata.get("raise_when_not_found"):
                    raise AttributeError("The key '%s' was not found in the env variables" % key)

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
