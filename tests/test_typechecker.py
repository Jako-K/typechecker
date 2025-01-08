import pytest
from typing import List, Tuple, Dict, Union, Optional
from typechecker import typecheck

def test_no_type_hints():
    @typecheck
    def func_no_hints(a, b):
        return a + b

    assert func_no_hints(3, 5) == 8
    assert func_no_hints("Hello ", "World") == "Hello World"


def test_simple_types():
    @typecheck
    def add_ints(a: int, b: int) -> int:
        return a + b

    assert add_ints(2, 3) == 5

    with pytest.raises(TypeError):
        add_ints("2", 3)


def test_list_of_ints():
    @typecheck
    def sum_list(numbers: List[int]) -> int:
        return sum(numbers)

    assert sum_list([1, 2, 3]) == 6

    with pytest.raises(TypeError):
        sum_list([1, "2", 3])  # "2" is not int


def test_tuple_of_strings():
    @typecheck
    def combine_tuple(strings: Tuple[str, ...]) -> str:
        return "-".join(strings)

    assert combine_tuple(("a", "b", "c")) == "a-b-c"
    with pytest.raises(TypeError):
        combine_tuple(("a", 123, "c"))


def test_dict_of_str_to_int():
    @typecheck
    def total_items(d: Dict[str, int]) -> int:
        return sum(d.values())

    d_ok = {"apples": 5, "oranges": 2}
    assert total_items(d_ok) == 7

    d_bad = {"apples": 5, "oranges": "some string"}
    with pytest.raises(TypeError):
        total_items(d_bad)


def test_union_arg():
    @typecheck
    def process_value(val: Union[int, str]) -> str:
        return str(val) + "_processed"

    assert process_value(42) == "42_processed"
    assert process_value("hello") == "hello_processed"
    with pytest.raises(TypeError):
        process_value([1, 2, 3])  # Not int or str


def test_union_return_type():
    @typecheck
    def maybe_none(flag: bool) -> Union[int, None]:
        return 42 if flag else None

    assert maybe_none(True) == 42
    assert maybe_none(False) is None


def test_optional():
    @typecheck
    def greet(name: Optional[str]) -> str:
        if name:
            return f"Hello, {name}!"
        return "Hello, Anonymous!"

    assert greet("Alice") == "Hello, Alice!"
    assert greet(None) == "Hello, Anonymous!"
    with pytest.raises(TypeError):
        greet(123)  # Not str or None


def test_nested_generics():
    @typecheck
    def nested(data: List[Dict[str, List[int]]]) -> int:
        total = 0
        for dictionary in data:
            for key, int_list in dictionary.items():
                total += sum(int_list)
        return total

    assert nested([{"numbers": [1, 2]}, {"more": [3, 4]}]) == 10
    with pytest.raises(TypeError):
        nested([{"numbers": [1, "not_int"]}])  # "not_int" is not int
