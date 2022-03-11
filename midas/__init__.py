import os
import json
import inspect
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

def test(format):
    def internal(func):
        test_name = func.__name__
        test_dir = os.path.dirname(func.__code__.co_filename)
        assert format == 'lines'

        in_path, gold_path, actual_path = get_midas_paths(test_dir, test_name)
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

SNAPSHOT_COUNTS = {}
def assert_snapshot(actual):
    result = repr(actual)
    test_name, test_dir = find_calling_test()
    if test_name not in SNAPSHOT_COUNTS:
        SNAPSHOT_COUNTS[test_name] = 0
    count = SNAPSHOT_COUNTS[test_name]
    SNAPSHOT_COUNTS[test_name] += 1

    snapshot_name = test_name + '__' + str(count)
    _in_path, gold_path, actual_path = get_midas_paths(test_dir, snapshot_name)
    try:
        with open(gold_path) as f:
            gold = f.read()
    except:
        logger.warning(f"No .gold file, maybe run mv {actual_path} {gold_path}")
        gold = None

    # we always want to write the actual result to a file
    with open(actual_path, 'w') as f:
        f.write(result)
    midas_assert(gold, result)

def find_calling_test():
    current_frame = inspect.currentframe()
    frames = inspect.getouterframes(current_frame, context=20)
    # 0 is us, 1 is assert_snapshot()
    for frame in frames[2:]:
        name = frame.function
        if name.startswith('test_'):
            return name, os.path.dirname(frame.filename)
    raise Exception('midas expects assert_snapshot() to be at most 20 function calls deep into a function called test_<something>()')

def get_midas_paths(test_dir, test_name):
    return (os.path.abspath(os.path.join(test_dir, test_name + '.in')),
        os.path.abspath(os.path.join(test_dir, test_name + '.gold')),
        os.path.abspath(os.path.join(test_dir, test_name + '.actual')))
