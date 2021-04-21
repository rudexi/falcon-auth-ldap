'''Setup script'''

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='falcon-auth-ldap',
    author='Guillaume Ludinard',
    author_email='guillaume.ludi@gmail.com',
    description='LDAP simple authentication for Falcon',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=[
        'falcon-auth',
        'ldap3',
    ],
    license='GPL3',
    packages=find_packages(),
    url='https://github.com/rudexi/falcon-auth-ldap',
)
