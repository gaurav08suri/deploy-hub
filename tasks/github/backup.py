import os
from datetime import datetime
from github import Github
from pyinfra.operations import git, server, pip, files
# from gh2md import gh2md

token = os.environ['GITHUB_ACCESS_TOKEN']
client = Github(token)
#  = 'xxxxxxxxx'
date_prefix = datetime.today().strftime('%Y-%m-%d')

# Fetch all repos of the organization
for repo in client.get_organization('dadabhagwan').get_repos():
    print(repo.name)

    files.directory(
        name='Ensure the /tmp/dir_that_we_want_removed is removed',
        path=f"./{date_prefix}/issues/{repo.name}",
        present=True,
    )

    if repo.name != 'mba-sys' or repo.archived:
        continue
    
    pip.venv(
        name='Create a virtual env',
        path='./venv'
    )

    pip.packages(
        packages=['gh2md'],
        virtualenv='./venv'
    )

    # git.repo(
    #     name='Clone repo',
    #     src='https://github.com/Fizzadar/pyinfra.git',
    #     dest='dest',
    #     # branch=None,  # use the default branch
    # )

    # server.shell(commands=[f"gh2md {repo.full_name} --multiple-files ./{date_prefix}/issues/{repo.name}"])

    # Clone the repo
    git.repo(
        src=repo.ssh_url,
        dest=f"{date_prefix}/{repo.full_name}",
        branch=None
    )
    # gh2md sarabander/sicp sicp-issues --multiple-files --no-closed-prs