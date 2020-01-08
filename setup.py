from distutils.core import setup

setup(
  name = 'py-schluter',
  packages = ['schluter'],
  version = '0.1.2',
  license='MIT',
  description = 'Python API for Schluter DITRA-HEAT thermostat',
  author = 'Adam Michaleski',
  author_email = 'adam@prairieapps.com',
  url = 'https://github.com/prairieapps/py-schluter',
  requires=['requests']
)