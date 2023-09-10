from setuptools import setup

setup(
    name='SwarmIntelligenceBackend',
    version='0.1.0',
    packages=['db', 'db.transactions', 'tests', 'models', 'routes', 'security'],
    package_dir={'': 'src'},
    url='https://github.com/Raphael2b3/SwarmIntelligenceBackend',
    license='GNU GPLv3',
    author='Raphael Schütz',
    author_email='raphael.schuetz0311@gmail.com',
    description='Backend for opensource swarmintelligence Application'
)
