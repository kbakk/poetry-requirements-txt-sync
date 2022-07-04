import pathlib
import subprocess
import sys
from typing import List, Optional

__version__ = "0.1.0"


def execute_sync_command(
    extras_name: str, requirements_txt_path: pathlib.Path, hashes=False
):
    cmd = (
        f"poetry export --format=requirements.txt "
        f"--extras {extras_name} "
        f"--output {requirements_txt_path}"
    )
    if hashes:
        cmd += " --without-hashes"
    print(cmd)
    run_res = subprocess.run(cmd.split())
    run_res.check_returncode()
    return


def cli():
    import typer

    def version_callback(value: bool):
        if value:
            typer.echo(f"{__version__}")
            raise typer.Exit()

    def pointer_callback(pointer: List[str]):
        for mapping in pointer:
            if len([i for i, c in enumerate(mapping) if c == ":"]) != 1:
                raise typer.BadParameter(
                    f"Bad format of {mapping=!r}, expected to find a single ':'"
                )
        return pointer

    def _cli(
        pointer: List[str] = typer.Option(..., callback=pointer_callback),
        _: Optional[bool] = typer.Option(
            None, "--version", callback=version_callback, is_eager=True
        ),
    ):
        exit_code = 0
        for extras_name, requirements_txt_path in (m.split(":") for m in pointer):
            try:
                execute_sync_command(
                    extras_name=extras_name,
                    requirements_txt_path=pathlib.Path(requirements_txt_path),
                )
            except subprocess.CalledProcessError as e:
                program = e.args[1][0]
                exit_code = e.args[0]
                typer.echo(
                    f"{program} exited with exit code {exit_code}, check output",
                    err=True,
                )
        sys.exit(0)

    typer.run(_cli)


if __name__ == "__main__":
    cli()
