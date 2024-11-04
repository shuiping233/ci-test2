import json
import os
from dataclasses import dataclass
from typing import TypedDict, TypeAlias
from pathlib import Path

from log import Log

IssueType: TypeAlias = str


class ConfigJson(TypedDict):
    class ProcessingAction(TypedDict):
        add_prefix: str
        add_suffix: str
        remove_keyword: list[str]

    rjust_space_width: int
    rjust_character: str
    table_separator: str
    archive_template: str
    archive_document_path: str
    action_name_map: dict[str, str]
    issue_title_processing_rules: dict[IssueType,
                                       ProcessingAction]


class Config():

    def __init__(self, config_path: str):
        self.rjust_space_width: int
        self.rjust_character: str
        self.archive_template: str
        self.archive_template: str
        self.archive_document_path: str
        self.table_separator: str
        self.action_name_map: dict[str, str]
        self.issue_title_processing_rules: dict[IssueType,
                                                ConfigJson.ProcessingAction]
        self.raw_json: ConfigJson = json.loads(
            Path(config_path).read_text(encoding="utf-8")
        )
        self.__dict__.update(self.raw_json)

