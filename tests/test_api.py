import midas

@midas.test(format='lines')
def test_length(line):
    return str(len(line))

"""
@midas.snapshot_test
def test_snapshot():
    midas.assert_snapshot('this is the first output')
    midas.assert_snapshot('this is the second output')
"""
