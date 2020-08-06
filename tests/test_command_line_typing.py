from unittest import mock

import pytest

from command_line_typing import command_line_typing


def mock_input(*args):
    input_values = list(args)

    def mock_input2(s=None):
        print(s, end="")
        return input_values.pop(0)

    return mock_input2


def test_load_practice_phrases(tmpdir):
    test_file = tmpdir.join("phrases")
    test_data = """[SHORT]
test line 1
test line 2
[MEDIUM]
medium 1
medium test 2
medium test 3
[LONG]
test long 1
long 2
long 3 test"""
    test_file.write(test_data)
    with mock.patch.object(command_line_typing, "FILE_NAME", test_file.strpath):
        short, medium, long = command_line_typing.load_practice_phrases()
    assert short == ["test line 1", "test line 2"]
    assert medium == ["medium 1", "medium test 2", "medium test 3"]
    assert long == ["test long 1", "long 2", "long 3 test"]


@pytest.mark.parametrize("test_typed, expected_result", [
    ("This is a test line for testing.", 0),
    ("This is a tast line for testing.", 1),
    ("This is a test lome for testing.", 2),
    ("this is a test line for testing", 2),
    # ("This is a test line for testings.", 1),  # broken
    ("This is a test lone far testing.", 2),
])
def test_check_for_mistakes(test_typed, expected_result):
    practice = "This is a test line for testing."
    result = command_line_typing.check_for_mistakes(practice, test_typed)
    assert result == expected_result


def test_practice_run_through_no_mistakes(capsys):
    command_line_typing.input = mock_input("This is a test line for testing.")
    command_line_typing.practice("This is a test line for testing.")
    captured = capsys.readouterr().out
    assert "Errors: 0" in captured
