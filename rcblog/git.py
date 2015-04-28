import sh


def commit(working_directory: str, files_to_commit: list, commit_message: str):
    sh.cd(working_directory)
    sh.git.add(*files_to_commit)
    # TODO Commit messages with several paragraphs
    sh.git.commit('-a', '-m', '{}'.format(commit_message))
