import bottle
from bottle import get, post, static_file, request, route, template
from bottle import SimpleTemplate
from configparser import ConfigParser
from ldap3 import Connection, LDAPBindError, LDAPInvalidCredentialsResult, Server
from ldap3 import AUTH_SIMPLE, SUBTREE
from os import path


@get('/')
def get_index():
    return index_tpl()


@post('/')
def post_index():
    form = request.forms.get

    def error(msg):
        return index_tpl(username=form('username'), alerts=[('error', msg)])

    if form('new-password') != form('confirm-password'):
        return error("Password doesn't match the confirmation!")

    if len(form('new-password')) < 8:
        return error("Password must be at least 8 characters long!")

    if not change_password(form('username'), form('old-password'), form('new-password')):
        print("Unsuccessful attemp to change password for: %s" % form('username'))
        return error("Username or password is incorrect!")

    print("Password successfully changed for: %s" % form('username'))

    return index_tpl(alerts=[('success', "Password has been changed")])


@route('/static/<filename>', name='static')
def serve_static(filename):
    return static_file(filename, root=path.join(BASE_DIR, 'static'))


def index_tpl(**kwargs):
    return template('index', **kwargs)


def change_password(username, old_pass, new_pass):
    server = Server(CONF['ldap']['host'], int(CONF['ldap']['port']))
    user_dn = find_user_dn(server, username)

    try:
        with Connection(server, authentication=AUTH_SIMPLE, raise_exceptions=True,
                        user=user_dn, password=old_pass) as c:
            c.bind()
            c.extend.standard.modify_password(user_dn, old_pass, new_pass)
        return True
    except (LDAPBindError, LDAPInvalidCredentialsResult):
        return False


def find_user_dn(server, uid):
    with Connection(server) as c:
        c.search(CONF['ldap']['base'], "(uid=%s)" % uid, SUBTREE, attributes=['dn'])
        return c.response[0]['dn'] if c.response else None


BASE_DIR = path.dirname(__file__)

CONF = ConfigParser()
CONF.read(path.join(BASE_DIR, 'settings.ini'))

bottle.TEMPLATE_PATH = [ BASE_DIR ]

# Set default attributes to pass into templates.
SimpleTemplate.defaults = dict(CONF['html'])
SimpleTemplate.defaults['url'] = bottle.url


# Run bottle internal test server when invoked directly (in development).
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080)
# Run bottle in application mode (in production under uWSGI server).
else:
    application = bottle.default_app()
