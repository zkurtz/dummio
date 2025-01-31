from pathlib import Path
from textwrap import dedent

from upath import UPath

import dummio
from dummio.constants import PathType

# example yaml string:
CONF = dedent("""
    # Simple config file
    defaults: &defaults
      timeout: 30
      retries: 3
      logging: true

    development:
      <<: *defaults
      logging: false
      settings:
        debug: true
    """).strip()


def _assert_yaml_content(oldpath: PathType, newpath: PathType) -> None:
    Path(oldpath).write_text(CONF)

    # Load the config using dummio:
    config = dummio.yaml.load(oldpath)

    # Assert some values:
    assert config["defaults"]["timeout"] == 30
    assert config["development"]["settings"]["debug"] is True
    assert config["development"]["retries"] == 3
    assert config["development"]["logging"] is False  # Inherited from defaults

    # Save the config back to a new file:
    dummio.yaml.save(config, filepath=newpath)

    # Load the new config as a string and compare vs the original string:
    conf_str = Path(newpath).read_text().strip()
    assert CONF == conf_str


def test_yaml(tmp_path: Path) -> None:
    oldpath = tmp_path / "config.yaml"
    newpath = tmp_path / "config_new.yaml"
    _assert_yaml_content(oldpath, newpath)
    _assert_yaml_content(str(oldpath), str(newpath))
    _assert_yaml_content(UPath(oldpath), UPath(newpath))
