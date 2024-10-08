from typing import Any, Dict, List, Literal, Tuple, Union

import pytest

from knot_resolver.utils.modeling import BaseSchema
from knot_resolver.utils.modeling.types import is_list, is_literal

types = [
    bool,
    int,
    str,
    Dict[Any, Any],
    Tuple[Any, Any],
    Union[str, int],
    BaseSchema,
]
literal_types = [Literal[5], Literal["test"], Literal[False]]


@pytest.mark.parametrize("val", types)
def test_is_list_true(val: Any):
    assert is_list(List[val])


@pytest.mark.parametrize("val", types)
def test_is_list_false(val: Any):
    assert not is_list(val)


@pytest.mark.parametrize("val", literal_types)
def test_is_literal_true(val: Any):
    assert is_literal(Literal[val])


@pytest.mark.parametrize("val", types)
def test_is_literal_false(val: Any):
    assert not is_literal(val)
