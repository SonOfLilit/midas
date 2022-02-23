import os
import json
import pytest
import logging

logger = logging.getLogger(__name__)

DEFAULT_INPUT = 'This is a midas inputs file. Write some test inputs, one per line (delete this text)'

# TODO: Tsvika said there is a way to tell pytest "this is the end of the stack"
def midas_assert(expected, actual):
    assert expected == actual

def strip_trailing_newline(s):
    if s.endswith('\r\n'):
        return s[:-2]
    if s.endswith('\n'):
        return s[:-1]
    return s
assert strip_trailing_newline('hello') == 'hello'
assert strip_trailing_newline('hello \n world') == 'hello \n world'
assert strip_trailing_newline('hello\n') == 'hello'
assert strip_trailing_newline('hello\r\n') == 'hello'
assert strip_trailing_newline('hello\r') == 'hello\r'
assert strip_trailing_newline('hello\n\n') == 'hello\n'

def golden_test(format):
    def internal(func):
        filename = func.__name__
        base_dir = os.path.dirname(func.__code__.co_filename)
        assert format == 'lines'

        in_path = os.path.abspath(os.path.join(base_dir, filename + '.in'))
        gold_path = os.path.abspath(os.path.join(base_dir, filename + '.gold'))
        actual_path = os.path.abspath(os.path.join(base_dir, filename + '.actual'))
        try:
            o = open(in_path, 'r')
        except:
            with open(in_path, 'w') as f:
                f.write(DEFAULT_INPUT)
            assert False, f"midas: inputs file did not exist, empty file created: {in_path}"
        with o as f:
            inputs = [strip_trailing_newline(line) for line in f.readlines()]
            if inputs == [DEFAULT_INPUT]:
                assert False, f"midas: must edit inputs file {in_path}"

        warning = None
        try:
            o = open(gold_path, 'r')
        except:
            warning = f"No .gold file, maybe run mv {actual_path} {gold_path}"
            expected = {}
        else:
            with o as f:
                expected = json.load(f)

        actual = {}
        testdata = [(line, expected.get(line)) for line in inputs]
        @pytest.mark.parametrize("line,expected", testdata)
        def test_func(line, expected):
            try:
                result = repr(func(line))
            except Exception as e:
                result = e.__class__.__name__
            actual[line] = result
            if len(actual) == len(testdata):
                with open(actual_path, 'w') as f:
                    json.dump(actual, f, indent=2, ensure_ascii=False)
            if warning is not None:
                logger.warning(warning)
            midas_assert(expected, result)
        return test_func
    return internal
