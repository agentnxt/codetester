from github import Github
from app.config import settings


class GitHubTools:
    def __init__(self):
        self.client = Github(settings.github_token) if settings.github_token else None

    def scan_repo(self, repo_name: str):
        if not self.client:
            return {"error": "Missing GitHub token"}

        repo = self.client.get_repo(repo_name)

        return {
            "name": repo.full_name,
            "description": repo.description,
            "default_branch": repo.default_branch,
            "open_issues": repo.open_issues_count,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "languages": repo.get_languages(),
            "recent_commits": [
                {
                    "sha": c.sha,
                    "message": c.commit.message,
                }
                for c in repo.get_commits()[:5]
            ],
            "workflows_detected": [
                ".github/workflows"
            ],
        }
