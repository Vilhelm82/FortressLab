from fortresslab import MODEL_VERSION, __version__


def test_package_exposes_independent_package_and_model_versions() -> None:
    assert __version__ == "0.1.0"
    assert MODEL_VERSION == "poc-foundation-1"
