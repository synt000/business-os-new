def test_import_app():
    from apps.main import app
    assert app is not None
