import os
import typer

REQUIRED_ENVS = ["OPENAI_API_KEY"]

def ensure_runtime_env():
    """
    Checks if all required environment variables are set.
    If not, prints the missing variables and exits with code 1.
    """
    missing = [k for k in REQUIRED_ENVS if not os.getenv(k)]

    if missing:
        typer.echo("❌ Missing environment variables:")
        for k in missing:
            typer.echo(f"  - {k}")

        typer.echo("\nSet it using:")
        typer.echo("export OPENAI_API_KEY=sk-xxxx")
        raise typer.Exit(code=1)
