import os
import re
import subprocess
from typing import List
from agent_schemas import GithubCopilotAgent


class GitCopilotUtils:
    def __init__(self):
        """
        Initializes a GitCopilotUtils object.

        This object contains methods for performing common git operations
        safely.
        """
        pass

    def get_current_git_branch(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        # try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.DEVNULL
            )
        print("Current branch:", branch.decode().strip())
        return {"branch_name": branch.decode().strip()}
        # except subprocess.CalledProcessError:
        #     return {"branch_name": ""}


    def git_unstaged_files(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Lists all the unstaged files.

        Returns:
            List[str]: List of file names in the current directory.
        """
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True, text=True
        )
        return {"unstaged_files": result.stdout.strip().splitlines()}

    def stage_files_safe(self, state: GithubCopilotAgent)-> GithubCopilotAgent:
        """
        Stages files in the current directory. If any of the files
        passed do not exist, prints a message and returns without
        staging any files.

        Args:
            files (List[str]): List of file names to stage

        Returns:
            subprocess.CompletedProcess: The result of the subprocess.
        """
        valid = [f for f in state["unstaged_files"] if os.path.exists(f)]
        if not valid:
            print("No valid files to stage")
            return {"staged_files": valid}

        result = subprocess.run(["git", "add"] + valid, check=True)
        return {"staged_files": valid}

    def get_staged_diff(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Returns the diff of all staged files (git diff --cached).

        Returns:
            str: Unified diff text.
        """
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True
        )
        return {"staged_files_diff": result.stdout.strip()}


    def commit_files(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Commits all the staged files with a given message.

        Args:
            message (str): The commit message.

        Returns:
            subprocess.CompletedProcess: The result of the subprocess.
        """
        commit_result = subprocess.run(["git", "commit", "-m", state['commit_message']], check=True)
        print("Files committed with message:", commit_result)
        return {}

    def push_branch(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Pushes the current branch to the remote repository.

        Args:
            branch (str, optional): The name of the branch to push. Defaults to "main".

        Returns:
            subprocess.CompletedProcess: The result of the subprocess.
        """
        resultl =  subprocess.run(["git", "push", "origin", state["branch_name"]], check=True)
        print("Branch pushed:", resultl)
        return {}
