import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = 'https://api.github.com'
GITHUB_PAT = os.getenv('GITHUB_PAT')


class GitHubAPIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def list_repositories():
    headers = {'Authorization': f'token {GITHUB_PAT}'}
    response = requests.get(f'{GITHUB_API_URL}/user/repos', headers=headers)
    if response.status_code != 200:
        raise GitHubAPIError("Failed to fetch repositories")
    return response.json()


import requests
# from .exceptions import GitHubAPIError


def invite_collaborator(owner, repo_name, username, permission='push'):
    headers = {'Authorization': f'token {GITHUB_PAT}'}
    response = requests.put(
        f'{GITHUB_API_URL}/repos/{owner}/{repo_name}/collaborators/{username}',
        headers=headers,
        json={'permission': permission}
    )

    if response.status_code == 201:
        return {"message": f"Invitation sent to {username} for repository {repo_name}"}
    raise GitHubAPIError(f"Failed to send invitation: {response.json()}")


def remove_collaborator(owner, repo_name, username):
    headers = {'Authorization': f'token {GITHUB_PAT}'}
    response = requests.delete(
        f'{GITHUB_API_URL}/repos/{owner}/{repo_name}/collaborators/{username}',
        headers=headers
    )
    if response.status_code != 204:
        raise GitHubAPIError(f"Failed to remove user: {response.json()}")
    return {"message": f"Removed {username} from repository {repo_name}"}


def revoke_all_access(username):
    repos = list_repositories()
    headers = {'Authorization': f'token {GITHUB_PAT}'}
    for repo in repos:
        repo_name = repo['name']
        owner = repo['owner']['login']  # Get owner from the repo data
        response = requests.delete(
            f'{GITHUB_API_URL}/repos/{owner}/{repo_name}/collaborators/{username}',
            headers=headers
        )
        if response.status_code != 204:
            raise GitHubAPIError(f"Failed to remove user from repo {repo_name}: {response.json()}")
    return {"message": f"Revoked all access for {username}"}
