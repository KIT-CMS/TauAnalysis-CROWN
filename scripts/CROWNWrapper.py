from __future__ import annotations  # needed for type annotations in > python 3.7

import contextvars
import inspect
import re
from contextlib import contextmanager
from typing import Any, Callable, Dict, Generator, List, Tuple, Union

from code_generation.configuration import Configuration, TConfiguration
from code_generation.producer import (
    BaseFilter as _BaseFilter,
    ExtendedVectorProducer as _ExtendedVectorProducer,
    Filter as _Filter,
    Producer as _Producer,
    ProducerGroup as _ProducerGroup,
    TProducerInput as _TProducerInput,
    VectorProducer as _VectorProducer,
)
from code_generation.quantity import QuantitiesInput
from code_generation.rules import ProducerRule
from code_generation.systematics import SystematicShift


CONTEXT_REGISTRY: Dict[str, contextvars.ContextVar] = {
    k: contextvars.ContextVar(k, default=None)
    for k in [
        "name",
        "scopes",
        "shift_key",
        "shift_map",
        "producers",
        "ignore_producers",
        "samples",
        "exclude_samples",
        "input",
        "subproducers",
        "call",
        "output",
        "vec_configs",
    ]
}


@contextmanager
def defaults(**kwargs: Any) -> Generator[None, None, None]:
    tokens = []
    try:
        for key, value in kwargs.items():
            try:
                tokens.append(CONTEXT_REGISTRY[key].set(value))
            except KeyError:
                raise ValueError(f"Unknown context variable: {key}")
        yield
    finally:
        for token in reversed(tokens):
            token.var.reset(token)


def get_adjusted_add_shift_SystematicShift(configuration: Configuration) -> Callable:
    def add_shift(
        # those can be set via the context manager defaults
        name: Union[str, None] = None,
        scopes: Union[str, Tuple[str, ...]] = None,
        shift_key: str = None,
        shift_map: Dict[str, Any] = None,
        producers: Union[Dict[Union[str, Tuple[str, ...]], List[object]], List[object]] = None,
        ignore_producers: Union[None, Dict[str, Any]] = None,
        samples: Union[str, List[str], None] = None,
        exclude_samples: Union[str, List[str], None] = None,
        # this can be set explicetly to capture more complex shift configurations (together with producers)
        shift_config: Union[Dict[str, Any], None] = None,
    ):
        # if shift_config is set it overrides shift_key and shift_map
        # if producers is procided as a dict it ignores scopes

        name = name or CONTEXT_REGISTRY["name"].get()
        scopes = scopes or CONTEXT_REGISTRY["scopes"].get()
        shift_key = shift_key or CONTEXT_REGISTRY["shift_key"].get()
        shift_map = shift_map or CONTEXT_REGISTRY["shift_map"].get()
        producers = producers or CONTEXT_REGISTRY["producers"].get()

        to_be_checked = (
            [name, shift_config, producers]
            if shift_config is not None and isinstance(producers, dict)
            else [name, scopes, shift_key, shift_map, producers]
        )

        if any(it is None for it in to_be_checked):
            raise ValueError(
                "scopes, shift_key, shift_map, and producers must be set."
            )

        for direction, value in shift_map.items() if shift_map else shift_config.items():
            configuration.add_shift(
                SystematicShift(
                    name=f"{name}{direction}",
                    shift_config=shift_config[direction] if shift_config else {
                        scopes: (
                            dict(zip(shift_key, value))
                            if all(
                                [
                                    isinstance(shift_key, (list, tuple)),
                                    isinstance(value, (list, tuple)),
                                    len(shift_key) == len(value),
                                ]
                            )
                            else {shift_key: value}
                        )
                    },
                    producers=producers if isinstance(producers, dict) else {scopes: producers},
                    ignore_producers=ignore_producers or CONTEXT_REGISTRY["ignore_producers"].get() or {},
                ),
                samples=samples or CONTEXT_REGISTRY["samples"].get(),
                exclude_samples=exclude_samples or CONTEXT_REGISTRY["exclude_samples"].get(),
            )
    return add_shift


def _get_variable_name():
    frame = inspect.currentframe().f_back.f_back
    code_context = inspect.getframeinfo(frame).code_context
    if code_context:
        call_line = code_context[0].strip()
        match = re.match(r"([\w\d_]+)\s*(=|:=)", call_line)
        if match:
            return match.group(1)
    raise RuntimeError("Could not determine variable name from context")


class MissingValue(Exception):
    def __init__(self, variable_name: str):
        super().__init__(
            f"Missing value for variable '{variable_name}'. "
            "Please provide a value either as an argument or "
            "through a 'with defaults(...)' context."
        )


class NameNotDetermined(Exception):
    def __init__(self):
        super().__init__(
            "Name could not be determined. "
            "This should not happened. Workaround: provide the name explicitly"
        )


class BaseFilter(_BaseFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("call", CONTEXT_REGISTRY["call"].get())
        kwargs.setdefault("input", CONTEXT_REGISTRY["input"].get())
        kwargs.setdefault("scopes", CONTEXT_REGISTRY["scopes"].get())

        if kwargs["name"] is None:
            raise NameNotDetermined

        for key in ["call", "input", "scopes"]:
            if kwargs[key] is None:
                raise MissingValue(key)

        super().__init__(*args, **kwargs)


class Filter(_Filter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("call", CONTEXT_REGISTRY["call"].get())
        kwargs.setdefault("input", CONTEXT_REGISTRY["input"].get())
        kwargs.setdefault("scopes", CONTEXT_REGISTRY["scopes"].get())
        kwargs.setdefault("subproducers", CONTEXT_REGISTRY["subproducers"].get())

        if kwargs["name"] is None:
            raise NameNotDetermined

        for key in ["call", "input", "scopes", "subproducers"]:
            if kwargs[key] is None:
                raise MissingValue(key)

        super().__init__(*args, **kwargs)


class Producer(_Producer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("call", CONTEXT_REGISTRY["call"].get())
        kwargs.setdefault("input", CONTEXT_REGISTRY["input"].get())
        kwargs.setdefault("scopes", CONTEXT_REGISTRY["scopes"].get())
        kwargs.setdefault("output", CONTEXT_REGISTRY["output"].get())

        if kwargs["name"] is None:
            raise NameNotDetermined

        for key in ["scopes", "input", "call", "output"]:
            if kwargs[key] is None:
                raise MissingValue(key)

        super().__init__(*args, **kwargs)


class ProducerGroup(_ProducerGroup):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("call", CONTEXT_REGISTRY["call"].get())
        kwargs.setdefault("input", CONTEXT_REGISTRY["input"].get())
        kwargs.setdefault("output", CONTEXT_REGISTRY["output"].get())
        kwargs.setdefault("scopes", CONTEXT_REGISTRY["scopes"].get())
        kwargs.setdefault("subproducers", CONTEXT_REGISTRY["subproducers"].get())

        if kwargs["name"] is None:
            raise NameNotDetermined

        for key in ["scopes", "subproducers"]:
            if kwargs[key] is None:
                raise MissingValue(key)

        super().__init__(*args, **kwargs)


class VectorProducer(_VectorProducer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("call", CONTEXT_REGISTRY["call"].get())
        kwargs.setdefault("input", CONTEXT_REGISTRY["input"].get())
        kwargs.setdefault("output", CONTEXT_REGISTRY["output"].get())
        kwargs.setdefault("scopes", CONTEXT_REGISTRY["scopes"].get())
        kwargs.setdefault("vec_configs", CONTEXT_REGISTRY["vec_configs"].get())

        if kwargs["name"] is None:
            raise NameNotDetermined

        for key in ["scopes", "input", "vec_configs", "call"]:
            if kwargs[key] is None:
                raise MissingValue(key)

        super().__init__(*args, **kwargs)


class ExtendedVectorProducer(_ExtendedVectorProducer):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", _get_variable_name())
        kwargs.setdefault("call", CONTEXT_REGISTRY["call"].get())
        kwargs.setdefault("input", CONTEXT_REGISTRY["input"].get())
        kwargs.setdefault("output", CONTEXT_REGISTRY["output"].get())
        kwargs.setdefault("scope", CONTEXT_REGISTRY["scopes"].get())
        kwargs.setdefault("vec_config", CONTEXT_REGISTRY["vec_configs"].get())

        if kwargs["name"] is None:
            raise NameNotDetermined

        for key in ["scope", "input", "output", "vec_config", "call"]:
            if kwargs[key] is None:
                raise MissingValue(key)

        super().__init__(*args, **kwargs)
