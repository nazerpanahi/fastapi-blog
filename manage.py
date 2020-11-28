from manager import Manager
from uvicorn import run

from conf import FAST_API_PORT

# https://pypi.org/project/manage.py
manager = Manager()


@manager.arg('port', 'p', help='Port that server runs on it')
@manager.arg('reload', 'r', help='Reload on every changes')
@manager.command(description='Run the server on the default port (settings.py)')
def runserver(port=FAST_API_PORT, reload=False):
    run('main:app', port=port, reload=reload)


if __name__ == '__main__':
    manager.main()
