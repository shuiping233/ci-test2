
import os
import sys
import json

from dispatch_schema import ClientPayload
from log import Log
from config import Config
from env import Env, should_run_in_github_action
from log import Log
from archive_document import ArchiveDocument


def load_local_env() -> None:
    print(Log.non_github_action_env)
    from dotenv import load_dotenv
    load_dotenv()


def get_config_path_from_args(args: list[str]) -> str:
    path = None
    if ("--config" in args):
        path = args[args.index("--config") + 1]
    if ("-c" in args != -1):
        path = args[args.index("-c") + 1]
    return path


def main(args: list[str]):
    if not should_run_in_github_action():
        load_local_env()
        
    config = Config(get_config_path_from_args(args))
    client_payload = ClientPayload(
        **json.loads(os.environ[Env.CLIENT_PAYLOAD])
    )
    archive_document = ArchiveDocument(
        config.archive_document_path
    )
    archive_document.archive_issue(
        rjust_character=config.rjust_character,
        rjust_space_width=config.rjust_space_width,
        table_separator=config.table_separator,
        archive_template=config.archive_template,
        issue_title_processing_rules=config.issue_title_processing_rules,
        issue_id=client_payload.issue_id,
        issue_type=client_payload.issue_type,
        issue_title=client_payload.issue_title,
        issue_repository=ArchiveDocument.action_name_to_repository_type(
            os.environ[Env.ACTION_NAME],
            config.action_name_map
        ),
        introduced_version=client_payload.introduced_version,
        archive_version=client_payload.archive_version
    )
    archive_document.save()
    archive_document.close()


if __name__ == "__main__":
    main(sys.argv)
