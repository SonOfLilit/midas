# Midas - Python Gold Testing Toolkit

If you're tired of writing assertions like `assert my_func('input') == 'output'`, just tell `midas` your inputs and it will automate all the rest!

## Installation

```
pip install midastest
```

## Usage

Write a test using your favorite testing framework. You can use any framework as long as it's `pytest`:

```
import midas

@midas.test(format='lines')
def test_length(line):
    return str(len(line))
```

Create a file `test_length.in` with a few examples:

```
Hello
Foo

What a wonderful world
```

Run your testing tool:

```
pytest
# TODO: show complaining output
```

After inspecting the output, move it to a file called `test_length.gold`:

```
mv test_length.actual test_length.gold
```

Run your testing tool again:

```
pytest
```

It succeeds!

What happened is that `test_length.gold` contains the expected inputs and outputs of the tests, and running the tests compares actual outputs with expected outputs:

```
cat test_length.gold
{
  "Hello": "'5'",
  "Foo": "'3'",
  "": "'0'",
  "What a wonderful world": "'22'"
}
```

Try changing the code:

```
import pytest

@midas.test(format='lines')
def test_length(line):
    return str(len(line) * 2)
```

Run `pytest` again and watch your tests fail:

```
==================================================================== test session starts =====================================================================
platform darwin -- Python 3.8.9, pytest-7.0.1, pluggy-1.0.0
rootdir: /Users/aursaraf/dev/dojo/midas
collected 4 items                                                                                                                                            

tests/test_api.py FF.F                                                                                                                                 [100%]

[..]
__________________________________________________________ test_length[What a wonderful world-'22'] __________________________________________________________

[..]
expected = "'22'", actual = "'44'"

    def midas_assert(expected, actual):
>       assert expected == actual
E       AssertionError

midas/__init__.py:12: AssertionError
================================================================== short test summary info ===================================================================
FAILED tests/test_api.py::test_length[Hello-'5'] - AssertionError
FAILED tests/test_api.py::test_length[Foo-'3'] - AssertionError
FAILED tests/test_api.py::test_length[What a wonderful world-'22'] - AssertionError
================================================================ 3 failed, 1 passed in 0.03s =================================================================
```

## License

`midas` is distributed under the MIT license.