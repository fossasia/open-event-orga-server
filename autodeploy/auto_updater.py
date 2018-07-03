import logging

from os.path import exists, isfile, join
from os import makedirs

from command import execute
from docker import DockerCompose, DockerComposeError
from git import Git

logger = logging.getLogger(__name__)


class AutoUpdater():
    def __init__(self, name, repo, cwd='.', branch='master'):
        self.name = name
        self.repo = repo
        self.cwd = cwd
        self.git = Git(repo, cwd, branch)
        self.docker = DockerCompose(cwd)

        self.container = None
        self.upgrade_script = None
        self.init_script = None

        if not exists(cwd):
            logger.info('<%s> creating missing directory %s', self.name, cwd)
            makedirs(cwd)
            self.git.clone_if_necessary()
            self.first_startup()

    def add_scripts(self, container='web', init_cmd='', upgrade_cmd=''):
        self.container = container
        self.init_script = init_cmd
        self.upgrade_script = upgrade_cmd

    def first_startup(self):
        self.docker.update()
        if self.init_script:
            try:
                res = self.docker.exec(self.container, upgrade_script)
                logger.info('<%s> initialized with %s', self.name, res)
            except DockerComposeError as e:
                logger.warning('%s: %s', e.message, e.errors)
        self.upgrade()

    def start(self):
        try:
            self.docker.start()
        except DockerComposeError as e:
            logger.warning('<%s> start threw an error: %s', self.name,
                           e.errors)

    def update(self):
        if self.git.changed_files() > 0:
            self.git.pull()
            self.docker.update()
            logger.info('<%s> update finished', self.name)
        else:
            logger.info('<%s> no update needed', self.name)

    def upgrade(self):
        if self.upgrade_script:
            try:
                res = self.docker.exec(self.container, self.upgrade_script)
                logger.info('<%s> upgraded with %s', self.name, res)
            except DockerComposeError as e:
                logger.warning('%s: %s', e.message, e.errors)
