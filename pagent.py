from langgraph.graph import StateGraph, START, END
from git_utils import GitCopilotUtils
from agent_schemas import GithubCopilotAgent
from review_agent import CommitMessageGenerator


gitUtils = GitCopilotUtils()
commitMessageGenerator = CommitMessageGenerator()
graph = StateGraph(GithubCopilotAgent)


graph.add_node("get_current_git_branch", gitUtils.get_current_git_branch)
graph.add_node("list_unstaged_files", gitUtils.git_unstaged_files)
graph.add_node("stage_files_safe", gitUtils.stage_files_safe)
graph.add_node("get_staged_diff", gitUtils.get_staged_diff)
graph.add_node("generate_commit_message", commitMessageGenerator.generate)
graph.add_node("commit_files", gitUtils.commit_files)
graph.add_node("push_branch", gitUtils.push_branch)

graph.add_edge(START, "get_current_git_branch")
graph.add_edge("get_current_git_branch", "list_unstaged_files")
graph.add_edge("list_unstaged_files", "stage_files_safe")
graph.add_edge("stage_files_safe", "get_staged_diff")
graph.add_edge("get_staged_diff", "generate_commit_message")
graph.add_edge("generate_commit_message", "commit_files")
graph.add_edge("commit_files", "push_branch")
graph.add_edge("push_branch", END)
app = graph.compile()


print("List files: ", app.invoke({}))

