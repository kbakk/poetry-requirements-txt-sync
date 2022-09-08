import pathlib
import subprocess
import sys

import tomli

__version__ = "0.2.0"


def execute_sync_command(
    extras_name: str, requirements_txt_path: pathlib.Path, hashes=True
):
    cmd = (
        f"poetry export --format=requirements.txt "
        f"--extras {extras_name} "
        f"--output {requirements_txt_path}"
    )
    if hashes is False:
        cmd += " --without-hashes"
    print(cmd)
    run_res = subprocess.run(cmd.split())
    run_res.check_returncode()
    return


def main():
    pyproject_path = "pyproject.toml" if len(sys.argv) == 1 else sys.argv[1]
    try:
        with open(pyproject_path, "rb") as fd:
            pyproject = tomli.load(fd)
    except OSError as err:
        print("Error loading pyproject file:", err)
        sys.exit(10)
    mapping = (
        pyproject.get("tool", {}).get("poetry-requirements-txt-sync", {}).get("map")
    )
    if mapping and isinstance(mapping, dict):
        for name, req_path in mapping.items():
            execute_sync_command(extras_name=name, requirements_txt_path=req_path)
    else:
        print(
            f"Error reading mapping in 'tool.poetry-requirements-txt-sync.map', expected key/value pairs, got {type(mapping)}"
        )
        sys.exit(20)


if __name__ == "__main__":
    main()
