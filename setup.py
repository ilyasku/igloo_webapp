"""
USAGE: 
   o install in develop mode: navigate to the folder containing this file,
                              and type 'python setup.py develop --user'.
                              (ommit '--user' if you want to install for 
                               all users)                           
"""
from setuptools import setup

setup(name='igloo_webapp',
      version='0.2.5',
      description='Run igloo random walk monte carlo simulations via web interface',
      url='',
      author='Ilyas Kuhlemann',
      author_email='ilyasp.ku@gmail.com',
      license='MIT',
      packages=["igloo_webapp",
                "igloo_webapp.model",
                "igloo_webapp.app",
                "igloo_webapp.persistence",
                "igloo_webapp.web"],
      entry_points={
          "console_scripts": [
          ],
          "gui_scripts": [
          ]
      },
      install_requires=["Flask",
                        "flask-wtf",
                        "wtforms",
                        "nose",
                        "click",
                        "matplotlib"],
      include_package_data=True,
      zip_safe=False)
