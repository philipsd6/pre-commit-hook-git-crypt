import argparse
import os.path
from shlex import quote
from typing import Optional
from typing import Sequence

from pre_commit_hooks.util import cmd_output
from pre_commit_hooks.util import CalledProcessError


def configured_for_git_crypt() -> bool:
    """git crypt init creates a directory inside the repository .git directory"""
    return os.path.isdir(os.path.join(".git", "git-crypt"))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", nargs="*", help="Filenames pre-commit believes are changed."
    )
    args = parser.parse_args(argv)

    if not configured_for_git_crypt():
        return 0

    try:
        cmd_output("git", "crypt", "status", "-e", *args.filenames)
    except CalledProcessError as e:
        stderr = e.args[-1].decode()
        if "is not a git command" in stderr:
            print(
                "Repository is configured for git-crypt, but git-crypt is not installed!"
            )
            return 1
        try:
            cmd_output("git", "crypt", "status", "-f")
            print("Fixed problems with the repository")
        except CalledProcessError as e:
            stderr = e.args[-1].decode()
            unencrypted_files = [
                quote(l.split(":")[1].strip()) for l in stderr.splitlines()
            ]
            print(
                "\n\t".join(
                    (
                        "Staged version is NOT ENCRYPTED! Run `git crypt status -e' to check; resolve with:",
                        "git restore --staged \\\n\t\t{files}",
                        "git crypt unlock",
                        "git add {files}",
                    )
                ).format(files="\n\t\t".join(unencrypted_files))
            )
            return 1


if __name__ == "__main__":
    exit(main())
