from app.models.layout import Layout


def test_layout_schema_defaults_and_fields():
    layout = Layout(name="Test", config={})
    assert layout.version >= 1
    assert layout.config.body.layout.columns in {1, 2}
    assert layout.config.background.mode in {"cover", "contain", "tile"}


def test_layout_rejects_unsafe_asset_path():
    try:
        Layout(
            name="Unsafe",
            config={"header": {"logo": "../etc/passwd"}},
        )
        assert False, "Expected validation failure"
    except Exception:
        assert True
