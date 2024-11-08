from pathlib import Path

from config import IssueType, ConfigJson
from exception import ErrorMessage


class ArchiveDocument():
    def __init__(self, path: str):

        with open(path, 'r', encoding="utf-8") as file:
            self.__lines = file.readlines()
            self.__new_lines: list[str] = []
            self.__reverse_lines = self.__lines[::-1]
        self.__file = open(path, 'w', encoding="utf-8")

    def __add_line(self, line: str) -> None:
        self.__new_lines.append(line)

    def __get_table_last_line_index(self) -> int:
        line_index = 0
        for index, line in enumerate(self.__reverse_lines, 1):
            if line.strip():
                line_index = index
                break
        return len(self.__lines) - line_index

    @staticmethod
    def action_name_to_repository_type(
        action_name: str,
        action_name_map: dict[str, str]
    ) -> str:
        result = action_name_map.get(action_name)
        if result is None:
            raise ValueError(ErrorMessage.unknown_action_name)
        return result

    def __get_last_table_number(
        self,
        table_separator: str
    ) -> int:
        table_last_line = self.__lines[
            self.__get_table_last_line_index()
        ]
        start = table_last_line.find(table_separator)
        end = table_last_line.find(table_separator, start+1)
        return int(table_last_line[start+1:end])

    @staticmethod
    def parse_issue_title(
        issue_title: str,
        issue_type: str,
        issue_title_processing_rules: dict[IssueType,
                                           ConfigJson.ProcessingAction]
    ) -> str:
        action_map = issue_title_processing_rules.get(
            issue_type)
        if action_map is None:
            return issue_title
        else:
            result = issue_title
            for keyword in action_map["remove_keyword"]:
                result.replace(keyword, '')
            result = ''.join(
                [action_map["add_prefix"],
                 result,
                 action_map["add_suffix"]]
            )
            return result

    def archive_issue(self,
                      rjust_space_width: int,
                      rjust_character: str,
                      table_separator: str,
                      archive_template: str,
                      issue_title_processing_rules: dict[IssueType,
                                                         ConfigJson.ProcessingAction],
                      issue_id: int,
                      issue_type: str,
                      issue_title: str,
                      issue_repository: str,
                      introduced_version: str,
                      archive_version: str
                      ) -> None:
        new_line = archive_template.format(
            table_id=self.__get_last_table_number(
                table_separator) + 1,

            issue_type=issue_type,
            issue_title=ArchiveDocument.parse_issue_title(
                issue_title,
                issue_type,
                issue_title_processing_rules
            ),
            rjust_space=((rjust_space_width
                          - len(issue_title))
                         * rjust_character),
            issue_repository=issue_repository,
            issue_id=issue_id,
            introduced_version=introduced_version,
            archive_version=archive_version
        )
        if "\n" not in new_line:
            new_line += "\n"
        self.__add_line(new_line)

    def save(self) -> None:
        self.__lines.insert(
            self.__get_table_last_line_index() + 1,
            *self.__new_lines
        )
        self.__file.writelines(
            self.__lines
        )

    def close(self) -> None:
        self.__file.close()
