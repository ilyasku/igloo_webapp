# IGLOO Webapp

Webapp to run [IGLOO](https://github.com/zerotonin/igloo) simulations.

# Deploy

## On Uberspace

### Create virtualenv

```
virtualenv ~/venvs/igloo
source ~/venvs/igloo/bin/activate
# we will use uwsgi to serve the web app:
pip install uwsgi
```

### Install igloo_webapp as wheel

Follow the instructions in the official flask tutorial for deployment.
I.e., pack your app as a wheel, copy the wheel file to the server,
and install it with pip in your virtualenv.

### Create ini files

One in a location of your choice, mine is in `~/web_apps/igloo.ini`:

```
[uwsgi]
mount = /igloo=igloo_webapp:app
manage-script-name=true
pidfile = igloo.pid
processes = 2
http-socket = :1025
chmod-socket = 660
vacuum = true
virtualenv = /home/ilyasnc/venvs/igloo
```

(My username on uberspace is ilyasnc.)
One in `~/etc/services.d/igloo.ini`:

```
[program:flask-igloo]
directory=%(ENV_HOME)s/web_apps
command=%(ENV_HOME)s/venvs/igloo/bin/uwsgi igloo.ini
```

`directory` has to point to the folder where you put the first `igloo.ini` in.

### `config.py`

The `config.py` file, where all the local app configurations need to go in,
has to be put in the app instance folder. With the config above, that is
`/home/ilyasnc/venvs/igloo/var/igloo_webapp.app-instance`. The config file
does not have to contain much:

```
SECRET_KEY = 'some_random_key'
SCRIPT_NAME = '/igloo'
```

### Configure uberspace web backend

A simple command is all it takes:

```
uberspace web backend set /igloo --http --port 1025
```

### Start service

Use these commands to start the app / restart the app
after installing a new version:

```
supervisorctl reread
supervisorctl update
supervisorctl restart flask-igloo
```

Check the status with `supervisorctl status`.