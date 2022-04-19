from typing import Any

import pytest
from jinja2 import Template

from knot_resolver_manager.datamodel.types import EscQuotesString, RawString
from knot_resolver_manager.utils.modelling import SchemaNode

str_template = Template('"{{ string }}"')


@pytest.mark.parametrize(
    "val,exp",
    [
        ("string", "string"),
        (2000, "2000"),
        ('"double quotes"', r"\"double quotes\""),
        ("'single quotes'", r"\'single quotes\'"),
        # fmt: off
        ('\"double quotes\"', r'\"double quotes\"'),
        ("\'single quotes\'", r'\'single quotes\''),
        # fmt: on
    ],
)
def test_esc_quotes_string(val: Any, exp: str):
    class TestSchema(SchemaNode):
        escaped: EscQuotesString

    d = TestSchema({"escaped": val})
    assert str_template.render(string=d.escaped) == f'"{exp}"'


@pytest.mark.parametrize(
    "val,exp",
    [
        ("string", "string"),
        (2000, "2000"),
        ('\n\t"', r"\n\t\""),
        ('"double quotes"', r"\"double quotes\""),
        ("'single quotes'", r"\'single quotes\'"),
        # fmt: off
        ('\"double quotes\"', r'\"double quotes\"'),
        ("\'single quotes\'", r'\'single quotes\''),
        # fmt: on
    ],
)
def test_raw_string(val: Any, exp: str):
    class TestSchema(SchemaNode):
        pattern: RawString

    d = TestSchema({"pattern": val})
    assert str_template.render(string=d.pattern) == f'"{exp}"'
