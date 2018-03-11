import logging

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1beta1.types import WriteResult
from github.Organization import Organization
from github.NamedUser import NamedUser
from github.Repository import Repository

from .utils import settings

logger = logging.getLogger(__name__)


class EthericFirebase:
    def __init__(self, test_name='899'):
        self._cred = credentials.Certificate(
            settings()['firebase'])

        self.client = firestore.client(app=self.app)
        self.github = self.client.collection('github')

    @property
    def app(self):
        try:
            _app = firebase_admin.get_app()
        except ValueError:
            _app = firebase_admin.initialize_app(
                self._cred, {'databaseURL':
                             'https://kittypad-d8e2d.firebaseio.com'})
        return _app

    def create_or_update_org(self, organization_id: str,
                             data: dict) -> WriteResult:
        """Creates or updates an organization in firebase

        Args:
            organization_id (str): Organization Name
            data (dict): Dict of organization information

        Returns:
            google.cloud.firestore_v1beta1.types.WriteResult

        """
        org = {
            'id': organization_id,
            'ghId': data['id'],
            'ghLogin': data.get('login'),
            'ghUrl': data.get('url'),
            'ghReposCount': data.get('public_repos'),
            'ghHtml': data.get('html_url'),
            'ghCreatedAt': data.get('created_at'),
            'ghUpdatedAt': data.get('updated_at'),
            'ghType': data.get('type'),
        }

        logger.info('Updating {} Organization'.format(organization_id))

        return (self.github
                .document('organisations')
                .collection(organization_id)
                .document('information')
                .set(org))


    def get_organization(self, organization_id: str) -> dict:
        """Retrieves organization from firebase

        Args:
            organization_id (str): Organization Name

        Returns:
            A dict of organization information.
        """
        return (self.client.collection('github')
                .document('organisations')
                .collection(organization_id)
                .document('information')
                .get()
                .to_dict())

    def create_or_update_repo(self, organization_id: str,
                              data: Repository) -> WriteResult:
        """Creates or updates """
        repo = {
            'id': data.get('id'),
            'name': data.get('name'),
            'fullName': data.get('full_name'),
            'isPrivate': data.get('private'),
            'htmlUrl': data.get('html_url'),
            'url': data.get('url'),
            'createdAt': data.get('created_at'),
            'updatedAt': data.get('updated_at'),
            'size': data.get('size'),
            'watchers': data.get('watchers'),
            'stars': data.stars,
            'hasIssues': data.get('has_issues'),
            'hasProjects': data.get('has_projects'),
            'hasDownloads': data.get('has_downloads'),
            'hasWiki': data.get('has_wiki'),
            'hasPages': data.get('has_pages'),
            'forksCount': data.get('forks_count'),
            'archived': data.get('archived'),
            'openIssues': data.get('open_issues'),
            'permissions': data.get('permissions'),
            'homepage': data.get('homepage')
        }
        logger.info('Updating {} repo : {}'.format(
            organization_id, data.get('name')))

        return (self.client
                .collection('github')
                .document('organisations')
                .collection(organization_id)
                .document(repo.name)
                .set(repo))

    def create_or_update_org_member(self, organization_id:str,
                                    data: dict) -> WriteResult:
        member = {
            'id': data.get('id'),
            'login': data.get('login'),
            'avatar': data.get('avatar_url'),
        }

        logger.info('Updating {} member: {}'.format(
            organization_id, data.get('login')))

        return (self.client
                .collection('github')
                .document('organisations')
                .collection(organization_id)
                .document('members')
                .collection('list')
                .document(member['id'])
                .set(member))

    def create_or_update_git_user(self, data: dict) -> WriteResult:
        user = {
            'id': data.get('id'),
            'login': data.get('login'),
            'name': data.get('name'),
            'company': data.get('company'),
            'blog': data.get('blog'),
            'location': data.get('location'),
            'email': data.get('email'),
            'hireable': data.get('hireable'),
            'bio': data.get('bio'),
            'avatar': data.get('avatar_url'),
            'reposCount': data.get('public_repos'),
            'gistsCount': data.get('public_gists'),
            'followers': data.get('followers'),
            'following': data.get('following'),
            'createdAt': data.get('created_at'),
            'updatedAt': data.get('updated_at')
        }

        logger.info('Updating git user: {}'.format(data.get('name')))

        return (self.client
                .collection('github')
                .document('users')
                .collection('list')
                .document(user['id'])
                .set(user))

    # Getters
    def get_all_coins(self):
        raise NotImplementedError

    def get_coin(self, coin_id: str):
        raise NotImplementedError

    def get_all_gh_org(self, coin_id: str):
        raise NotImplementedError

    def get_gh_org(self, coin_id: str):
        raise NotImplementedError

    def get_gh_org_repos(self, coin_id: str):
        raise NotImplementedError

    def get_gh_org_members(self, coin_id: str):
        raise NotImplementedError

    # Other
    def add_coin(self, coin):
        raise NotImplementedError

    def _add_field_data_if_valid(self, obj, key: str, value: str):
        if value:
            obj[key] = value

if __name__ == '__main__':
    e = EthericFirebase()
    print(e.get_organization('Ethereum'))