import logging
from typing import Union

import github
from github import Github, Organization, Repository, PaginatedList

from .firebase import EthericFirebase
from .utils import settings

logger = logging.getLogger(__name__)

class Client:
    '''
    Notes:
        - 5000 requests/hr authenticated, 60/hr unauth.
        - Conditional requests: Responses have `last_modified` field, can use to decide which re-request.
          If the resource hasn't changed, returns `304 Not Modified`
        - Which functions make most requests, which pages lend themselves to scrapy?
        - Class, Module Naming convention?
    '''
    def __init__(self):
        creds = settings()['github']
        self.client = Github(client_id=creds['id'],
                             client_secret=creds['secret'])
        self.firebase = EthericFirebase()


    def fetch_org_info(self, organization_id: str) -> Organization:
        """This does not return the fields:
            `has_organization_projects` or `has_repository_projects`

        import requests
        BASE_URL = 'https://api.github.com/{}/{}?clientid={}&client_secret={}'

        url = BASE_URL.format('orgs', organization_id, GIT_ID, GIT_SECRET)
        org = requests.get(url)"""

        org = self.client.get_organization(organization_id)
        repos = org.get_repos()
        members = org.get_public_members()

        if org:
            self.firebase.create_or_update_org(organization_id,
                                               org.raw_data)

        if repos:
            self.firebase.create_or_update_repo(organization_id,
                                                repos.raw_data)
        if members:
            for member in members:
                self.firebase.create_or_update_org_member(
                    organization_id, member.raw_data)

        return org


    def fetch_org_repos(self, organization: Organization) -> PaginatedList:
        """Fetches organization repos

        pygithub returns: `github.PaginatedList.PaginatedList` of
        `github.Repository.Repository`

            :param organization_id:
        """
        repos = organization.get_repos()
        return repos

    def fetch_org_members(self, organization_id: str) -> PaginatedList:
        org = self.fetch_org_info(organization_id)
        members = org.get_public_members()
        return members

    def fetch_github_user_info(self, user_login: str) -> NamedUser:
        # I think the pygithub takes care of this
        user = self.client.get_user(user_login)
        self.firebase.create_or_update_git_user(user.raw_data)
        raise NotImplementedError

    def fetch_repo_info(self, repo_id: str) -> Repository:
        repo = self.client.get_repo(repo_id)
        return repo

    def fetch_repo_collaborators(
            self,
            repo_id: Union[Repository.Repository, str]) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)

        collabs = repo_id.get_collaborators()
        return collabs

    def fetch_repo_commits(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        commits = repo_id.get_commits()

        return commits

    def fetch_repo_tags(self,
                        repo_id: Union[Repository.Repository, str]) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        tags = repo_id.get_tags()

        return tags

    def fetch_repo_releases(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        releases = repo_id.get_releases()

        return releases

    def fetch_repo_languages(self, repo_id: str) ->PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        langs = repo_id.get_languages()

        return langs

    def fetch_repo_contributors(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        contribs = repo_id.get_collaborators()

        return contribs

    def fetch_repo_branches(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        branches = repo_id.get_branches()

        return branches

    def fetch_repo_issues(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        issues = repo_id.get_issues()

        return issues

    def fetch_repo_milestones(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        milestones = repo_id.get_milestones()

        return milestones

    def fetch_repo_teams(self, repo_id: str) -> PaginatedList:
        if isinstance(repo_id, str):
            repo_id = self.fetch_repo_info(repo_id)
        teams = repo_id.get_teams()

        return teams

    def fetch_repo_starred_by(self, repo_id: str) -> PaginatedList:
        # pygithub does not implement this, can just manually.
        pass

    def fetch_user_followers(self, user_id: str) -> PaginatedList:
        if isinstance(user_id, str):
            user_id = self.fetch_user_info(user_id)
        followers = user_id.get_followers()

        return followers

    def fetch_user_following(self, user_id: str) -> PaginatedList:
        if isinstance(user_id, str):
            user_id = self.fetch_user_info(user_id)
        following = user_id.get_following()

        return following


    def fetch_user_starred_repo(self, user_id: str) -> PaginatedList:
        if isinstance(user_id, str):
            user_id = self.fetch_user_info(user_id)
        starred = user_id.get_starred()

        return starred

    def fetch_user_teams(self, user_id: str) -> PaginatedList:
        # PyGithub doesnt implement a team... but can search org
        if isinstance(user_id, str):
            user_id = self.fetch_user_info(user_id)
        orgs = user_id.get_orgs()
        raise NotImplementedError