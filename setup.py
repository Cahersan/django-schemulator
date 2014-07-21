import os
from setuptools import setup
from pip.req import parse_requirements

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# requirements
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='django-schemulator',
    version='0.0.1',
    packages=['schemulator'],
    include_package_data=True,
    install_requires=reqs,    
    license='',
    description='Generate JSONSchema representations from Django forms',
    long_description=README,
    url='https://github.com/Cahersan/django-schemulator',
    author='Carlos de las Heras',
    author_email='cahersan@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
