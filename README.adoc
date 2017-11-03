= Web UI for changing LDAP password
Jakub Jirutka <https://github.com/jirutka[@jirutka]>
//custom
:proj-name: ldap-passwd-webui
:gh-name: jirutka/{proj-name}
:wikip-url: https://en.wikipedia.org/wiki
:pypi-url: https://pypi.python.org/pypi

The aim of this project is to provide a very simple web form for users to be able to change their password stored in LDAP or Active Directory (Samba 4 AD).
It’s built with http://bottlepy.org[Bottle], a WSGI micro web-framework for Python.


== Installation

=== Alpine Linux

. Install package *ldap-passwd-webui-waitress* from the Alpine’s community repository:
+
[source, sh]
apk add ldap-passwd-webui-waitress
+
IMPORTANT: This package is in Alpine stable since v3.7. You can also install it from _edge_ (unstable) branch.

. Adjust configuration in `/etc/ldap-passwd-webui.ini` and `/etc/conf.d/`.

. Start service ldap-passwd-webui:
+
[source]
/etc/init.d/ldap-passwd-webui start

=== Manually

Clone this repository and install dependencies:

[source, sh, subs="+attributes"]
----
git clone git@github.com:{gh-name}.git
cd {proj-name}
pip install -r requirements.txt
----

Read the next sections to learn how to run it.

=== Requirements

* Python 3.x
* {pypi-url}/bottle/[bottle]
* {pypi-url}/ldap3[ldap3] 2.x


== Configuration

Configuration is read from the file link:settings.ini.example[settings.ini].
You may change location of the settings file using the environment variable `CONF_FILE`.

If you have Active Directory (or Samba 4 AD), then you *must* use encrypted connection (i.e. LDAPS or StartTLS) – AD doesn’t allow changing password via unencrypted connection.


== Run it

There are multiple ways how to run it:

* with the built-in default WSGI server based on https://docs.python.org/3/library/wsgiref.html#module-wsgiref.simple_server[wsgiref],
* under a {wikip-url}/Web_Server_Gateway_Interface[WSGI] server like https://uwsgi-docs.readthedocs.org[uWSGI], https://docs.pylonsproject.org/projects/waitress[Waitress], http://gunicorn.org[Gunicorn], … (recommended)
* as a {wikip-url}/Common_Gateway_Interface[CGI] script.

=== Run with the built-in server

Simply execute the `app.py`:

[source, python]
python3 app.py

Then you can access the app on http://localhost:8080.
The port and host may be changed in link:settings.ini.example[settings.ini].


=== Run with Waitress

[source, sh, subs="+attributes"]
----
cd {proj-name}
waitress-serve --listen=*:8080 app:application
----

=== Run with uWSGI and nginx

If you have many micro-apps like this, it’s IMO kinda overkill to run each in a separate uWSGI process, isn’t it?
It’s not so well known, but uWSGI allows to “mount” multiple application in a single uWSGI process and with a single socket.

[source, ini, subs="+attributes"]
.Sample uWSGI configuration:
----
[uwsgi]
plugins = python3
socket = /run/uwsgi/main.sock
chdir = /var/www/scripts
logger = file:/var/log/uwsgi/main.log
processes = 1
threads = 2
# map URI paths to applications
mount = /admin/{proj-name}={proj-name}/app.py
#mount = /admin/change-world=change-world/app.py
manage-script-name = true
----

[source, nginx]
.Sample nginx configuration as a reverse proxy in front of uWSGI:
----
server {
    listen 443 ssl;
    server_name example.org;

    ssl_certificate     /etc/ssl/nginx/nginx.crt;
    ssl_certificate_key /etc/ssl/nginx/nginx.key;

    # uWSGI scripts
    location /admin/ {
        uwsgi_pass  unix:/run/uwsgi/main.sock;
        include     uwsgi_params;
    }
}
----

== Screenshot

image::doc/screenshot.png[]


== License

This project is licensed under http://opensource.org/licenses/MIT/[MIT License].
For the full text of the license, see the link:LICENSE[LICENSE] file.
