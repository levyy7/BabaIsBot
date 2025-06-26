import json
import os
import pytest


class MemoryStub:
    """
    A simple in-memory stub to simulate LongTermMemory behavior.
    """
    def __init__(self, initial_meanings):
        self._meanings = initial_meanings
        self.updated = None

    def get_property_meanings(self):
        return self._meanings

    def set_property_meanings(self, new_meanings):
        self.updated = new_meanings

@pytest.fixture(scope="session")
def fixtures_memory_0_0():
    with open('tests/fixtures/data/memory_0-BabaIsYou_0.json', 'r') as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="session")
def fixtures_memory_4_0():
    with open('tests/fixtures/data/memory_4-StillOutOfReach_0.json', 'r') as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="session")
def fixtures_memory_4_1():
    with open('tests/fixtures/data/memory_4-StillOutOfReach_1.json', 'r') as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="session")
def fixtures_memory_5_0():
    with open('tests/fixtures/data/memory_5-Volcano_0.json', 'r') as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="session")
def fixtures_memory_5_1():
    with open('tests/fixtures/data/memory_5-Volcano_1.json', 'r') as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="session")
def fixtures_memory_5_3():
    with open('tests/fixtures/data/memory_5-Volcano_3.json', 'r') as f:
        data = json.load(f)
    return data