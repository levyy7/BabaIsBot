import json
import pytest


# Wrap dicts into objects whose str() returns JSON
class DummyState:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return json.dumps(self.data)


@pytest.fixture(scope="function")
def fixtures_state_0_0():
    with open("tests/fixtures/data/state_0-BabaIsYou_0_actual.json", "r") as f:
        previous = json.load(f)
    with open("tests/fixtures/data/state_0-BabaIsYou_0_expected.json", "r") as f:
        expected = json.load(f)
    with open("tests/fixtures/data/state_0-BabaIsYou_0_actual.json", "r") as f:
        actual = json.load(f)
    return previous, expected, actual


@pytest.fixture(scope="function")
def fixtures_state_4_0():
    with open("tests/fixtures/data/state_4-StillOutOfReach_0_previous.json", "r") as f:
        previous = json.load(f)
    with open("tests/fixtures/data/state_4-StillOutOfReach_0_expected.json", "r") as f:
        expected = json.load(f)
    with open("tests/fixtures/data/state_4-StillOutOfReach_0_actual.json", "r") as f:
        actual = json.load(f)
    return previous, expected, actual


@pytest.fixture(scope="function")
def fixtures_state_4_1():
    with open("tests/fixtures/data/state_4-StillOutOfReach_1_previous.json", "r") as f:
        previous = json.load(f)
    with open("tests/fixtures/data/state_4-StillOutOfReach_1_expected.json", "r") as f:
        expected = json.load(f)
    with open("tests/fixtures/data/state_4-StillOutOfReach_1_actual.json", "r") as f:
        actual = json.load(f)
    return previous, expected, actual


@pytest.fixture(scope="function")
def fixtures_state_5_0():
    with open("tests/fixtures/data/state_5-Volcano_0_previous.json", "r") as f:
        previous = json.load(f)
    with open("tests/fixtures/data/state_5-Volcano_0_expected.json", "r") as f:
        expected = json.load(f)
    with open("tests/fixtures/data/state_5-Volcano_0_actual.json", "r") as f:
        actual = json.load(f)
    return previous, expected, actual


@pytest.fixture(scope="function")
def fixtures_state_5_1():
    with open("tests/fixtures/data/state_5-Volcano_1_previous.json", "r") as f:
        previous = json.load(f)
    with open("tests/fixtures/data/state_5-Volcano_1_expected.json", "r") as f:
        expected = json.load(f)
    with open("tests/fixtures/data/state_5-Volcano_1_actual.json", "r") as f:
        actual = json.load(f)
    return previous, expected, actual


@pytest.fixture(scope="function")
def fixtures_state_5_2():
    with open("tests/fixtures/data/state_5-Volcano_2_previous.json", "r") as f:
        previous = json.load(f)
    with open("tests/fixtures/data/state_5-Volcano_2_expected.json", "r") as f:
        expected = json.load(f)
    with open("tests/fixtures/data/state_5-Volcano_2_actual.json", "r") as f:
        actual = json.load(f)
    return previous, expected, actual
