import pylox


def test_version():
    assert isinstance(pylox.__version__, str)
