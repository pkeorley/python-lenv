# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

from os import getenv

from dotenv import load_dotenv


DEFAULT_DOTENV_FILE = ".env"


def _load_dotenv(dotenv_path: str = None):
    if not hasattr(_load_dotenv, "_loaded_dotenv_files"):
        _load_dotenv.already_loaded = []

    if dotenv_path in _load_dotenv.already_loaded:
        return

    if dotenv_path is None:
        dotenv_path = DEFAULT_DOTENV_FILE

    _load_dotenv.already_loaded.append(dotenv_path)

    load_dotenv(
        dotenv_path=dotenv_path,
    )


class Meta(type):
    def __new__(cls, name, bases, dct):
        heir = super().__new__(cls, name, bases, dct)

        _load_dotenv()

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
