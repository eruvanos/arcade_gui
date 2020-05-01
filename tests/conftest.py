from pytest import fixture

from tests import TestUIView


@fixture
def view() -> TestUIView:
    return TestUIView()
