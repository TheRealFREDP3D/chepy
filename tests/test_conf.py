from pathlib import Path
from chepy.conf import Config


def test_config():
    config = Config()
    config_dir = Path.home() / ".chepy"
    assert config.history_path == str(config_dir / "chepy_history")
    assert str(config.chepy_conf) == str(config_dir / "chepy.conf")
    assert Path(config.chepy_conf).exists()
    assert Path(config.history_path).exists()
