import typer
from gitcopilot.runtime import ensure_runtime_env
from core.pagent import run_agent

app = typer.Typer(
    help="GitCopilot – AI-powered Git CLI",
    invoke_without_command=True
)


@app.callback()
def main():
    """
    Run GitCopilot (default command)
    """
    ensure_runtime_env()
    run_agent()


if __name__ == "__main__":
    app()
