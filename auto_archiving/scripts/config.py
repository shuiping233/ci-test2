import json
import os
from dataclasses import dataclass
from typing import TypedDict
from pathlib import Path

from log import Log


class ConfigJson(TypedDict):
    rjust_space_width: int
    rjust_character: str
    table_separator: str
    archive_template: str
    archive_document_path: str


class Config():
    def __init__(self, config_path: str):
        self.rjust_space_width: int
        self.rjust_character: str
        self.archive_template: str
        self.archive_template: str
        self.archive_document_path: str
        self.table_separator: str
        self.raw_json: ConfigJson = json.loads(
            Path(config_path).read_text(encoding="utf-8")
        )
        self.__dict__.update(self.raw_json)
