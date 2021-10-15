import os
from datetime import datetime
from github import Github
from pyinfra.operations import git, server, pip, files

token = os.environ['GITHUB_ACCESS_TOKEN']
client = Github(token)

date_prefix = datetime.today().strftime('%Y-%m-%d')

pip.venv(
    name='Create a virtual env',
    path='./venv'
)

pip.packages(
    packages=['gh2md'],
    virtualenv='./venv'
)


# Fetch all repos of the organization
for repo in client.get_organization('dadabhagwan').get_repos():
    print(repo.name)

    # Skip archived repos
    if repo.archived:
        continue

    # Create directory
    files.directory(
        name=f"Ensure the {date_prefix}/issues/{repo.name} is present",
        path=f"./{date_prefix}/issues/{repo.name}",
        present=True,
    )

    # Export all PRs and Issues
    server.shell(commands=[f"gh2md {repo.full_name} --multiple-files ./{date_prefix}/issues/{repo.name}"])

    # Clone the repo
    git.repo(
        src=repo.ssh_url,
        dest=f"{date_prefix}/{repo.full_name}",
        branch=None,
        ssh_keyscan=True
    )