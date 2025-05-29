#!/usr/bin/env python3
"""Generic utilities for github org client.
"""
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)

__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access nested map with key path.
    Parameters
    ----------
    nested_map: Mapping
        A nested map
    path: Sequence
        a sequence of key representing a path to the value
    Example
    -------
    >>> nested_map = {"a": {"b": {"c": 1}}}
    >>> access_nested_map(nested_map, ["a", "b", "c"])
    1
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]

    return nested_map


def get_json(url: str) -> Dict:
    """Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """Decorator to memoize a method.
    Example
    -------
    class MyClass:
        @memoize
        def a_method(self):
            print("a_method called")
            return 42
    >>> my_object = MyClass()
    >>> my_object.a_method
    a_method called
    42
    >>> my_object.a_method
    42
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        """"memoized wraps"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)

"""
def run_tests():
    print("Running standalone tests...\n")

    # Success cases
    print("Test 1: Normal nested access")
    nested = {"a": {"b": {"c": 1}}}
    assert access_nested_map(nested, ["a", "b", "c"]) == 1
    print("Passed ✔️")

    print("Test 2: Root level access")
    nested = {"x": 42}
    assert access_nested_map(nested, ["x"]) == 42
    print("Passed ✔️")

    # KeyError - missing key
    print("Test 3: Missing key (should raise KeyError)")
    nested = {"a": {"b": 2}}
    try:
        access_nested_map(nested, ["a", "x"])
    except KeyError as e:
        print(f"Passed ✔️ (Caught KeyError: {e})")
    else:
        print("❌ Failed: Expected KeyError")

    # KeyError - non-mapping mid-path
    print("Test 4: Non-mapping mid-path (should raise KeyError)")
    nested = {"a": 5}
    try:
        access_nested_map(nested, ["a", "b"])
    except KeyError as e:
        print(f"Passed ✔️ (Caught KeyError: {e})")
    else:
        print("❌ Failed: Expected KeyError")

if __name__ == "__main__":
    run_tests()
"""