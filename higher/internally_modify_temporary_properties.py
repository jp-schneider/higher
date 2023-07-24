from typing import Any, Dict
import logging
from .temporary_properties import TemporaryProperties, NOTSET

class InternallyModifyTemporaryProperties(TemporaryProperties):
    """Context manager for altering a object temporary and set properties back to their original value.
    Sets the internally modify flag when setting / removing the values, but keep it on default (before value) within the block.
    """

    def __enter__(self):
        with TemporaryProperties(self.obj, _being_modified_internally=True):
            for k, v in self.intermediate_values.items():
                self.old_values[k] = getattr(self.obj, k, NOTSET)
                if self.old_values[k] == NOTSET:
                    logging.warning(f"Property: {k} was not existing in: {repr(self.obj)}!")
                setattr(self.obj, k, v)

    def __exit__(self, type, value, traceback):
        with TemporaryProperties(self.obj, _being_modified_internally=True):
            for k, v in self.old_values.items():
                if v == NOTSET:
                    delattr(self.obj, k)
                else:
                    setattr(self.obj, k, v)
        return False
