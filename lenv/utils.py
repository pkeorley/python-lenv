# Copyright © 2024 pkeorley
#
# This source code is licensed under the MIT license found in the LICENSE
# file in the root directory of this source tree.

import json
import typing as t


T = t.TypeVar("T")


def deserialize(value: t.Optional[str], type: t.Type[T]) -> T:
    if value is None:
        return None

    elif type == int:
        return int(value)

    elif type == str:
        return str(value)

    elif type == list:
        if not value.startswith("["):
            raise ValueError("Provided value is not a list")
        return json.loads(value)

    raise TypeError(f"Type {type} not supported")


def _getattr(__o: object, __name: str) -> t.Optional[t.Any]:
    """
    This function, like the standard library function `getattr`, returns the specified attribute,
    but without throwing an `AttributeError` if the attribute does not exist, in which case the output will be `None`

    >>> o = object()
    >>> print(getattr(o, "foo"))
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: 'object' object has no attribute 'foo'

    >>> print(_getattr(o, "foo"))
    None

    :param __o: Object
    :param __name: Attribute name
    :return: Attribute value
    """
    if hasattr(__o, __name):
        return getattr(__o, __name)
    return
