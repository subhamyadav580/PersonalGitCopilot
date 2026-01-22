from typing import Any, TypedDict, List



class GithubCopilotAgent(TypedDict):
    branch_name: str
    unstaged_files: List[str]
    staged_files: List[str]
    staged_files_diff: str
    commit_message: str