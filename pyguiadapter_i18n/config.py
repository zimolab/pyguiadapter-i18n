import dataclasses
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
APP_CONFIG_FILE_PATH = BASE_DIR / "config.json"

@dataclasses.dataclass
class Config(object):
    language: str = "en"


    def save_to(self, file_path: str | Path):
        config_dict = dataclasses.asdict(self)
        with open(file_path, "w") as f:
            f.write(json.dumps(config_dict, ensure_ascii=False, indent=4))


    @classmethod
    def load_from(cls, file_path: str | Path) -> "Config":
        if not Path(file_path).is_file():
            cls().save_to(file_path)
        with open(file_path, "r") as f:
            config_dict = json.loads(f.read())
        return cls(**config_dict)

    @classmethod
    def safe_load_from(cls, file_path: str | Path) -> "Config":
        try:
            return cls.load_from(file_path)
        except Exception as e:
            print(f"Error loading config file: {e}", file=sys.stderr)
            print(f"Using default config", file=sys.stderr)
            default_config = cls()
            default_config.save_to(file_path)
            return default_config