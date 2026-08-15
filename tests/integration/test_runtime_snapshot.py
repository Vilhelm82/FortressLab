import platform

from fortresslab import __version__
from fortresslab.manifest import collect_runtime_snapshot


def test_runtime_snapshot_reads_installed_versions() -> None:
    snapshot = collect_runtime_snapshot()
    assert snapshot.package_version == __version__
    assert snapshot.python_version == platform.python_version()
    assert snapshot.dependencies[0].name == "pydantic"
    assert snapshot.dependencies[0].version
