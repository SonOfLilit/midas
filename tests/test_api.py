import midas

@midas.golden_test(format='lines')
def test_length(line):
    return str(2 * len(line))
