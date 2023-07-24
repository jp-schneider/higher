from typing import Any, Dict
import logging

class _NOTSET():
    pass


NOTSET = _NOTSET()
"""Constant for a non existing value."""


class TemporaryProperties():
    """Context manager for altering a object temporary and set properties back to their original value."""

    def __init__(self, obj: Any, **kwargs):
        """Creates the context manager by an object and kwargs defining the 
        properties to alter with their value.

        Parameters
        ----------
        obj : Any
            The object which should be altered.

        kwargs:
            Property names and values to alter.

        Raises
        ------
        ArgumentNoneError
            If obj is None.
        """
        if obj is None:
            raise ValueError("obj is None!")
        self.obj = obj
        self.old_values = dict()
        self.intermediate_values = kwargs

    def __enter__(self):
        for k, v in self.intermediate_values.items():
            self.old_values[k] = getattr(self.obj, k, NOTSET)
            if self.old_values[k] == NOTSET:
                logging.warning(f"Property: {k} was not existing in: {repr(self.obj)}!")
            setattr(self.obj, k, v)

    def __exit__(self, type, value, traceback):
        for k, v in self.old_values.items():
            if v == NOTSET:
                delattr(self.obj, k)
            else:
                setattr(self.obj, k, v)
        return False
