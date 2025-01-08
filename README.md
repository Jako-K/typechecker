# **Typechecker**

Typechecker is a lightweight Python library for validating function arguments and return values using type hints. It integrates seamlessly with Python's type annotations.

---

## **Features**
- Automatic runtime type checking for function arguments and return values.
- Supports complex types, including List, Dict, Tuple, Union, Optional, and nested generics.
- Works with instance methods, class methods, and static methods.
- Includes helpful error messages with truncated collections for better readability.

---

## **Installation**
Install Typechecker with pip:
```
pip install typechecker
```
---


### **Basic Example**
Typecheck ensures that function arguments and return types adhere to type hints:

```python
from typechecker import typecheck

@typecheck
def add(a: int, b: int) -> int:
    return a + b

add(1, 2) # passes
add(1, "two") # raises `TypeError`
```

---

### **Complex Types**
Typecheck supports complex types such as `List`, `Dict`, and `Union`:

```python
from typing import List, Dict, Union
from typechecker import typecheck

@typecheck
def process_data(data: List[Dict[str, Union[int, None]]]) -> int:
    return sum(item.get("value", 0) for item in data)

process_data([{"value": 10}, {"value": None}]) # passes
process_data([{"value": "10"}]) # raises `TypeError`
```

---

### **Class Methods**
Typecheck works with instance methods, class methods, and static methods:

```python
class MyClass:
    @typecheck
    def instance_method(self, x: int) -> int:
        return x + 1
    
    @classmethod
    @typecheck
    def class_method(cls, numbers: List[int]) -> int:
        return sum(numbers)
    
    @staticmethod
    @typecheck
    def static_method(x: int, y: int) -> int:
        return x * y

obj = MyClass()  
obj.instance_method(5) # passes  
MyClass.class_method([1, 2, 3]) # passes  
MyClass.static_method(3, 4) # passes
```

