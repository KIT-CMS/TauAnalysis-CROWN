from __future__ import annotations  # needed for type annotations in > python 3.7

import inspect
import re
from contextlib import contextmanager
from contextvars import ContextVar
from typing import List, Union

from code_generation.configuration import Configuration, TConfiguration
from code_generation.producer import (
    BaseFilter,
    ExtendedVectorProducer,
    Filter,
    Producer,
    ProducerGroup,
    TProducerInput,
    VectorProducer,
)
from code_generation.quantity import QuantitiesInput
from code_generation.rules import ProducerRule

_default_scopes = ContextVar("default_scopes", default=None)


@contextmanager
def scopes(scopes):
    token = _default_scopes.set(scopes)
    try:
        yield
    finally:
        _default_scopes.reset(token)


def _get_variable_name():
    frame = inspect.currentframe().f_back.f_back
    code_context = inspect.getframeinfo(frame).code_context
    if code_context:
        call_line = code_context[0].strip()
        match = re.match(r"([\w\d_]+)\s*=", call_line)
        if match:
            return match.group(1)
    raise RuntimeError("Could not determine variable name from context")


class AutoBaseFilter(BaseFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("scopes", _default_scopes.get())
        super().__init__(*args, **kwargs)


class AutoFilter(Filter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("scopes", _default_scopes.get())
        super().__init__(*args, **kwargs)


class AutoProducer(Producer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("scopes", _default_scopes.get())
        super().__init__(*args, **kwargs)


class AutoProducerGroup(ProducerGroup):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("scopes", _default_scopes.get())
        super().__init__(*args, **kwargs)


class AutoVectorProducer(VectorProducer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("scopes", _default_scopes.get())
        super().__init__(*args, **kwargs)


class AutoExtendedVectorProducer(ExtendedVectorProducer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("scope", _default_scopes.get())
        super().__init__(*args, **kwargs)

class AutoConfiguration(Configuration):
    """
    A wrapper around the base Configuration class that allows setting scopes
    via a context manager. This allows to either call the methods with
    the scopes as the first argument, or to use the `scopes` context manager
    and omit the scopes argument.

    Example:
    >>> from .scripts.ConfigurationWrapper import Configuration, scopes
    >>> config = Configuration(...)
    >>> with scopes("global"):
    ...     config.add_producers([...]) # scopes is automatically "global"
    >>> config.add_producers("mt", [...]) # scopes is explicitly "mt"
    """

    def add_config_parameters(self, *args: Union[TConfiguration, str, List[str]]):
        if len(args) == 1:
            scopes_val = _default_scopes.get()
            if scopes_val is None:
                raise ValueError(
                    "scopes must be provided either as an argument or through a 'with scopes(...):' context."
                )
            super().add_config_parameters(scopes_val, args[0])
        else:
            super().add_config_parameters(*args)

    def add_producers(self, *args: Union[TProducerInput, str, List[str]]):
        if len(args) == 1:
            scopes_val = _default_scopes.get()
            if scopes_val is None:
                raise ValueError(
                    "scopes must be provided either as an argument or through a 'with scopes(...):' context."
                )
            super().add_producers(scopes_val, args[0])
        else:
            super().add_producers(*args)

    def add_outputs(self, *args: Union[QuantitiesInput, str, List[str]]):
        if len(args) == 1:
            scopes_val = _default_scopes.get()
            if scopes_val is None:
                raise ValueError(
                    "scopes must be provided either as an argument or through a 'with scopes(...):' context."
                )
            super().add_outputs(scopes_val, args[0])
        else:
            super().add_outputs(*args)

    def add_modification_rule(self, *args: Union[ProducerRule, str, List[str]]):
        if len(args) == 1:
            scopes_val = _default_scopes.get()
            if scopes_val is None:
                raise ValueError(
                    "scopes must be provided either as an argument or through a 'with scopes(...):' context."
                )
            super().add_modification_rule(scopes_val, args[0])
        else:
            super().add_modification_rule(*args)
