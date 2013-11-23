"""Management utilities."""


from fabric.contrib.console import confirm
from fabric.api import abort, env, local, settings, task


# GLOBALS
env.run = 'python manage.py'
# END GLOBALS


# HELPERS
def cont(cmd, message):
    """Given a command, ``cmd``, and a message, ``message``, allow a user to
    either continue or break execution if errors occur while executing ``cmd``.

    :param str cmd: The command to execute on the local system.
    :param str message: The message to display to the user on failure.

    .. note::
        ``message`` should be phrased in the form of a question, as if 
        ``cmd``'s execution fails, we'll ask the user to press 'y' or 'n' to 
        continue or cancel exeuction, respectively.

    Usage::

        cont('heroku run ...', 
             "Couldn't complete {cmd}. Continue anyway?".format(cmd=cmd)
    """
    with settings(warn_only=True):
        result = local(cmd, capture=True)

    if message and result.failed and not confirm(message):
        abort('Stopped execution per user request.')
# END HELPERS


# DATABASE MANAGEMENT
@task
def syncdb():
    """Run a syncdb."""
    local('{run} syncdb --noinput'.format(**env))


@task
def migrate(app=None):
    """Apply one (or more) migrations. If no app is specified, fabric will
    attempt to run a site-wide migration.

    :param str app: Django app name to migrate.
    """
    if app:
        local('{run} migrate {app} --noinput'.format(app=app, **env))
    else:
        local('{run} migrate --noinput'.format(**env))

@task
def south_init(app):
    local('python manage.py schemamigration {app} --initial'.format(app=app))

@task
def south_update(app):
    local('python manage.py schemamigration {app} --auto'.format(app=app))
# END DATABASE MANAGEMENT


#LOCAL FILE MANAGEMENT
@task
def collectstatic():
    """Collect all static files"""
    local('{run} collectstatic --noinput'.format(**env))


@task
def compress():
    """Compress css and javascript files"""
    local('{run} compress'.format(**env))
# END FILE MANAGEMENT


# PROJECT MANAGEMENT
@task
def initialize():
    """Initialize local project after startproject"""
    local('rm -rf docs README.md')
    local('echo /{{ project_name }}/static >> .gitignore')
    local('echo /{{ project_name }}/media >> .gitignore')
    local('git flow init -d')
    local('git add .')
    local("git commit -m 'First commit'")

@task
def startapp(app):
    """Start a new django app"""
    local('git flow feature start {app}'.format(app=app))
    local('mkdir {{ project_name }}/apps/{app}'.format(app=app))
    local('python manage.py startapp {app} {{ project_name }}/apps/{app}'
            .format(app=app))
# END PROJECT MANAGEMENT
