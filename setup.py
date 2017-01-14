from sunshine import __version__
from distutilis import setup

setup (
    name = 'sunshine',
    version = __version__,
    description = 'Controls Philips Hue bulbs based on time and outside temprature',
    author = 'Joel Shaw',
    license = 'MIT',
    url = 'https://github.com/joelshaw/sunshine',
    py_modules = ['sunshine']
)
