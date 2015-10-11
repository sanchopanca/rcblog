import sh
import os
from pathlib import Path


def commit(working_directory: Path, files_to_commit: list, commit_message: str):
    os.chdir(str(working_directory))
    sh.git.add(*files_to_commit)
    # TODO Commit messages with several paragraphs
    sh.git.commit('-a', '-m', '{}'.format(commit_message))


def create_repository(working_directory: Path):
    os.chdir(str(working_directory))
    sh.git('init')
