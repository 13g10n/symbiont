import pytest

from symbiont.components import _ModuleMeta, Module


@pytest.fixture
def empty_module():
    class TestModule(Module):
        pass

    return TestModule


def test_module_meta_defaults():
    meta = _ModuleMeta()

    assert meta.imports == []
    assert meta.providers == []


def test_module_meta_generated(empty_module):
    assert isinstance(empty_module.meta, _ModuleMeta)
