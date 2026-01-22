import os
import re
import subprocess
from typing import List

from regex import F
from agent_schemas import GithubCopilotAgent
from langgraph.graph import END


class GitCopilotUtils:
    def __init__(self):
        """
        Initializes a GitCopilotUtils object.

        This object contains methods for performing common git operations
        safely.
        """
        self.EXCLUDE_DIRS = {
            ".cache",
            "node_modules",
            ".npm",
            ".venv",
            "Library",
            "Applications",
        }




    def find_git_repos(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        repos = []
        print("Searching for git repositories...")
        for dirpath, dirnames, _ in os.walk(os.path.expanduser("~")):
            dirnames[:] = [d for d in dirnames if d not in self.EXCLUDE_DIRS]

            if ".git" in dirnames:
                repos.append(dirpath)
                dirnames[:] = []

        return {"repos_list": repos}

    def get_current_git_branch(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Gets the current git branch.

        Returns:
            GithubCopilotAgent: AgentState with the current branch name.
        """
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.DEVNULL
            )
        return {"branch_name": branch.decode().strip()}


    def git_unstaged_files(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Lists all the unstaged files.

        Returns:
            GithubCopilotAgent: AgentState with the list of unstaged files.
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
            state (GithubCopilotAgent): AgentState with the list of unstaged files.

        Returns:
            GithubCopilotAgent: AgentState with the list of staged files.
        """
        valid = [f for f in state["unstaged_files"] if os.path.exists(f)]
        if not valid:
            print("No valid files to stage")
            return {"staged_files": valid}

        result = subprocess.run(["git", "add"] + valid, check=True)
        return {"staged_files": valid}

    def get_staged_diff(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Gets the diff of the staged files.

        Returns:
            GithubCopilotAgent: AgentState with the diff of the staged files.
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
            state (GithubCopilotAgent): AgentState with the commit message.

        Returns:
            GithubCopilotAgent: AgentState with no additional information.

        """
        commit_result = subprocess.run(["git", "commit", "-m", state['commit_message']], check=True)
        print("Files committed with message:", commit_result)
        return {}

    def push_branch(self, state: GithubCopilotAgent) -> GithubCopilotAgent:

        """
        Pushes the current branch to the remote repository.

        Args:
            state (GithubCopilotAgent): AgentState with the branch name.

        Returns:
            GithubCopilotAgent: AgentState with no additional information.
        """
        resultl =  subprocess.run(["git", "push", "origin", state["branch_name"]], check=True)
        print("Branch pushed:", resultl)
        return {}

    def check_files_to_commit(self, state: GithubCopilotAgent) -> GithubCopilotAgent:
        """
        Checks if there are any staged files to commit.

        Args:
            state (GithubCopilotAgent): AgentState with the staged files diff.

        Returns:
            GithubCopilotAgent: AgentState with a boolean indicating if there are staged files.
        """
        if len(state["staged_files_diff"]) > 0:
            return {"has_staged_files": True}
        else:
            print("No files to commit.")
            return {"has_staged_files": False}