
import os
import json
from pathlib import Path
import io

from dispatch_schema import ClientPayload
from log import Log
from config import Config

CONFIG_PATH = "./configs/config.json"


class ArchiveDocument():
    def __init__(self, path: str):
        self.__file = open(Path(path), 'r+', encoding="utf-8")
        self.__lines = self.__file.readlines()
        self.__new_lines: list[str] = []
        self.__reverse_lines = self.__lines[::-1]

    def __add_line(self, line: str) -> None:
        self.__new_lines.append(line)

    def __get_table_last_line_index(self) -> int:
        line_index = 0
        for index, line in enumerate(self.__reverse_lines, 1):
            if line.strip():
                line_index = index
                break
        return len(self.__lines) - line_index

    def __get_last_table_number(
        self,
        table_separator: str
    ) -> int:
        table_last_line = self.__lines[
            self.__get_table_last_line_index()
        ]
        start = table_last_line.find(table_separator)
        end = table_last_line.find(table_separator, start+1)
        return int(table_last_line[start+1, end])

    def archive_issue(self,
                      rjust_space_width: int,
                      rjust_character: str,
                      table_separator: str,
                      archive_template: str,
                      issue_id: int,
                      issue_type: str,
                      issue_title: str,
                      issue_repository: str,
                      introduced_version: str,
                      archive_version: str
                      ) -> None:
        
        # TODO
        self.__add_line(
            archive_template
            .format(
                table_id=self.__get_last_table_number(
                    table_separator) + 1,
                
                issue_type=issue_type,
                issue_title=issue_title,
                rjust_space = ((rjust_space_width 
                               - len(issue_title))
                               * rjust_character),
                issue_repository=issue_repository,
                issue_id=issue_id,
                introduced_version=introduced_version,
                archive_version=archive_version
            )
        )

    def save(self) -> None:
        self.__file.writelines(self.__new_lines)

    def close(self) -> None:
        self.__file.close()


def load_local_env() -> None:
    if os.environ.get("GITHUB_ACTIONS") != "true":
        print(Log.non_github_action_env)
        from dotenv import load_dotenv
        load_dotenv()


def main():
    load_local_env()
    config = Config(CONFIG_PATH)
    client_payload = ClientPayload(
        issue_repository=os.environ["GITHUB_REPOSITORY"],
        **json.loads(os.environ["CLIENT_PAYLOAD"])
    )
    archive_document = ArchiveDocument(
        config.archive_document_path
    )
    archive_document.archive_issue(
        rjust_character=config.rjust_character,
        rjust_space_width=config.rjust_space_width,
        table_separator=config.table_separator,
        archive_template=config.archive_template,
        **client_payload
    )


if __name__ == "__main__":
    main()
