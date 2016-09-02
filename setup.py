from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='go',
    version='0.2',
    description='Handy tool for connecting to servers via SSH',
    long_description=readme,
    author='Eric Beahan',
    author_email='ebeahan@gmail.com',
    url='https://github.com/ebeahan/go',
    packages=['go'],
    install_requires=[
        'SQLAlchemy',
        'future',
    ],
    scripts=['go/go.py']
)
