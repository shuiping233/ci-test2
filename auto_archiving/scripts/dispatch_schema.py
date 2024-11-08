from typing import TypedDict
from dataclasses import dataclass

from exception import ErrorMessage

class DispatchSchema(TypedDict):

    issue_id: int
    issue_type: str
    issue_title: str
    issue_state: str
    '''值只可能为 open 或 closed'''
    introduced_version: str
    archive_version: str

    # 判断外部和内部issue似乎可以从dispatch测判断


@dataclass()
class ClientPayload():
    issue_id: int
    issue_type: str
    issue_title: str
    issue_state: str
    '''值只可能为 open 或 closed'''
    introduced_version: str
    archive_version: str
