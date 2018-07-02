import logging

from command import execute

logger = logging.getLogger(__name__)


class DockerComposeError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.message = message
        self.errors = errors

    def __str__(self):
        return '{}:\n {}'.format(self.message, self.errors)


def _docker_compose(cwd, *cmd):
    retcode, out, err = execute(cwd, '/usr/bin/docker-compose', *cmd)
    if retcode == 0:
        return out

    logger.error('docker-compose failed: %s', cwd)
    raise DockerComposeError('docker-compose exited with a non-zero exit code',
                             err)


class DockerCompose():
    def __init__(self, cwd):
        self.cwd = cwd

    def ps(self):
        return _docker_compose(self.cwd, 'ps')

    def start(self):
        logger.info('starting up...')
        res = _docker_compose(self.cwd, 'start')
        logger.info('started')
        return res

    def stop(self):
        logger.info('stopping...')
        res = _docker_compose(self.cwd, 'stop')
        logger.info('stopped')
        return res

    def restart(self):
        logger.info('restarting...')
        res = _docker_compose(self.cwd, 'restart')
        logger.info('restarted')
        return res

    def build(self):
        logger.info('building...')
        res = _docker_compose(self.cwd, 'build')
        logger.info('(re-)built')
        return res
