# IGLOO Webapp

Webapp to run [IGLOO]() simulations.

# Deploy

This webapp was built with the [Flask framework](http://flask.pocoo.org/). So it should be possible
to deploy it following their [deployment instructions](http://flask.pocoo.org/docs/1.0/tutorial/deploy/).  
However, we probably didn't adhere to all guidelines, so I had to fix some things manually on the server
running Apache2 with `mod_wsgi` when I wanted to deploy it:

1. Run the `igloo-webapp-init-config-and-database` script. I created a folder `/var/www/igloo_webapp`
   into which I copied the `static` and the `templates` folder (that was the easiest way for me to grant apache access to these folders). If you do the same, you should type `/var/www/igloo_webapp/templates` and
   `/var/www/igloo_webapp/static` when the script prompts you for the locations of templates and static folders.

2. Since I couldn't get Apache to start my app as my process (i.e., it would always start as a process of root or some special apache user), I created the tiny script `igloo-web-copy-config-to-etc`. It works nicely with sudo on my arch machine, but did not work on raspbian (since a sudo also changes home directory on raspbian I think). If it does not work, you can also copy the config file manually. The default location is `~/.config/igloo_webapp.json`. Copy it to `/etc/`.

3. I ran into issues with writing to the database from the apache process. You need to give read+write access to the `sqlite` file as well as the folder! (The folder is the data folder you specified in step 1.) I think the same is true for the `tmp_current_simulation_*` folders that the processes write into while the simulations are running.

## `wsgi` File I Used on Raspberry Pi:
File `/var/www/igloo_webapp/igloo_webapp.wsgi`: 
```
# !/usr/bin/python3
activate_this = '/home/pi/virtualenvs/igloo/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
#execfile(activate_this, dict(__file__=activate_this))

from igloo_webapp.app import app as application
```

## Apache conf File I used on Raspberry Pi:

```
# file /etc/apache2/sites-available/igloo.conf:
<VirtualHost *:80>
  ServerName 192.168.0.101

  WSGIDaemonProcess igloo_webapp user=pi group=pi home=/home/pi threads=2
  WSGIScriptAlias / /var/www/igloo_webapp/igloo_webapp.wsgi

  <Directory /var/www/igloo_webapp>
    Require all granted
  </Directory>
</VirtualHost>
```
This could then be enabled with Apache's command: `a2ensite igloo`.