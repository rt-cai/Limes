from typing import Callable, TypeVar, Union

K = TypeVar('K')
T = TypeVar('T')
def Switch(arg: K, options: dict[Union[K, frozenset[K]], Callable[[], T]], default: Callable[[], T] = lambda: None) -> Union[T, None]:
    enter = False
    for key, fn in options.items():
        if (isinstance(arg, set) and arg in key) or arg == key:
            return fn()
    return default()
