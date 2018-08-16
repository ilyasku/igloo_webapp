"""
USAGE: 
   o install in develop mode: navigate to the folder containing this file,
                              and type 'python setup.py develop --user'.
                              (ommit '--user' if you want to install for 
                               all users)                           
"""
from setuptools import setup

setup(name='igloo_webapp',
      version='0.0.4',
      description='Run igloo random walk monte carlo simulations via web interface',
      url='',
      author='Bart Geurten, Ilyas Kuhlemann',
      author_email='bgeurte@gwdg.de',
      license='MIT',
      packages=["igloo_webapp",
                "igloo_webapp.CLI",
                "igloo_webapp.model",
                "igloo_webapp.app",
                "igloo_webapp.persistence",
                "igloo_webapp.web"],
      entry_points={
          "console_scripts": [
              "igloo-web-start-server=igloo_webapp.CLI.run_app:main",
              "igloo-web-init-config-and-database=igloo_webapp.CLI.init_config_and_folders:main",
              "igloo-web-copy-config-to-etc=igloo_webapp.CLI.copy_config_to_etc:main"
          ],
          "gui_scripts": [
          ]
      },
      install_requires=["Flask",
                        "flask-wtf",
                        "wtforms",
                        "nose"],
      zip_safe=False)
