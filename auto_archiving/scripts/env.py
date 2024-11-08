import os

class Env():
    ACTION_NAME = "ACTION_NAME"
    CLIENT_PAYLOAD = "CLIENT_PAYLOAD"
    GITHUB_ACTIONS = "GITHUB_ACTIONS"

def should_run_in_github_action() -> bool:
    return os.environ.get(Env.GITHUB_ACTIONS) == "true"