import pytest
import main

oldDict = {
    '1111111111111111111111111111111111111111': 'file 1.txt'
}

newDict = {
    '2222222222222222222222222222222222222222': 'file 2.txt'
}


@pytest.mark.parametrize('left, right, expected', [
    (oldDict, oldDict, {'old': {}, 'new': {}}),
    (oldDict, {}, {'old': oldDict, 'new': {}}),
    ({}, newDict, {'old': {}, 'new': newDict}),
    (oldDict, newDict, {'old': oldDict, 'new': newDict}),
    # one new, one old, one same
    (
        {
            '1111111111111111111111111111111111111111': 'file 1.txt',
            '2222222222222222222222222222222222222222': 'file 2.txt'
        },
        {
            '2222222222222222222222222222222222222222': 'file 2.txt',
            '3333333333333333333333333333333333333333': 'file 3.txt'
        },
        {
            'old': {'1111111111111111111111111111111111111111': 'file 1.txt'},
            'new': {'3333333333333333333333333333333333333333': 'file 3.txt'}
        }
    ),
    # one new, one old, one same sha1 but diff name
    (
        {
            '1111111111111111111111111111111111111111': 'file 1.txt',
            '2222222222222222222222222222222222222222': 'file 3.txt'
        },
        {
            '2222222222222222222222222222222222222222': 'file 4.txt',
            '3333333333333333333333333333333333333333': 'file 3.txt'
        },
        {
            'old': {'1111111111111111111111111111111111111111': 'file 1.txt'},
            'new': {'3333333333333333333333333333333333333333': 'file 3.txt'}
        }
    ),
    # one new and one old same file name, diff sha1
    (
        {
            '1111111111111111111111111111111111111111': 'file 1.txt',
            '2222222222222222222222222222222222222222': 'file 3.txt'
        },
        {
            '2222222222222222222222222222222222222222': 'file 4.txt',
            '3333333333333333333333333333333333333333': 'file 1.txt'
        },
        {
            'old': {'1111111111111111111111111111111111111111': 'file 1.txt'},
            'new': {'3333333333333333333333333333333333333333': 'file 1.txt'}
        }
    )

])
def test_getSymmetricDifference(left, right, expected):
    res = main.getSymmetricDifference(left.copy(), right.copy())
    assert res == expected
