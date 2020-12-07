from __future__ import absolute_import, unicode_literals
from manager import Manager
from uvicorn import run

from broker import celery

from conf.settings import FAST_API_PORT

# https://pypi.org/project/manage.py
manager = Manager()


@manager.arg('port', 'p', help='Port that server runs on it')
@manager.arg('reload', 'r', help='Reload on every changes')
@manager.command(description='Run the server on the default port (settings.py)')
def runserver(port=FAST_API_PORT, reload=False):
    run('main:app', port=port, reload=reload)


@manager.command(description="Run the celery server")
def runcelery():
    argv = [
        'worker',
        '-l',
        'INFO'
    ]
    celery.app.start(argv)


if __name__ == '__main__':
    manager.main()
