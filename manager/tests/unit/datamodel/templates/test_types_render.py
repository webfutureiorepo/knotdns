from typing import Any

import pytest
from jinja2 import Template

from knot_resolver_manager.datamodel.types import EscQuotesStr
from knot_resolver_manager.utils.modelling import SchemaNode


@pytest.mark.parametrize(
    "val,exp",
    [
        ("string", "string"),
        (2000, "2000"),
        ('"double quotes"', r"\"double quotes\""),
        ("'single quotes'", r"\'single quotes\'"),
        # fmt: off
        ('\"double quotes\"', r"\"double quotes\""),
        ("\'single quotes\'", r"\'single quotes\'"),
        # fmt: on
    ],
)
def test_escaped_quotes_string(val: Any, exp: str):
    class TestSchema(SchemaNode):
        escaped: EscQuotesStr

    d = TestSchema({"escaped": val})
    tmpl = Template('"{{ string }}"')
    assert tmpl.render(string=d.escaped) == f'"{exp}"'
