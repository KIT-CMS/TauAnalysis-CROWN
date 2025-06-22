import inspect
import re
from contextlib import contextmanager
from contextvars import ContextVar

from code_generation.producer import (
    BaseFilter,
    Filter,
    Producer,
    ProducerGroup,
    VectorProducer,
    ExtendedVectorProducer,
)

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
        kwargs.setdefault("scopes", _default_scopes.get())
        super().__init__(*args, **kwargs)
