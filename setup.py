"""
USAGE: 
   o install in develop mode: navigate to the folder containing this file,
                              and type 'python setup.py develop --user'.
                              (ommit '--user' if you want to install for 
                               all users)                           
"""
from setuptools import setup

setup(name='igloo_webapp',
      version='0.0.1',
      description='Run igloo random walk monte carlo simulations via web interface',
      url='',
      author='Bart Geurten, Ilyas Kuhlemann',
      author_email='bgeurte@gwdg.de',
      license='MIT',
      packages=["igloo_webapp"],
      entry_points={
          "console_scripts": [
              "igloo-web-start-server=igloo_webapp.CLI.run_app:main"
          ],
          "gui_scripts": [
          ]
      },
      install_requires=["Flask",
                        "flask-wtf",
                        "wtforms",
                        "nose"],
      zip_safe=False)
