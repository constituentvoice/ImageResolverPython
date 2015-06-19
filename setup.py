from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os
import sys

# attempt to pull version
sys.path.append('./imageresolver')
from version import __version__

setup(
	name='ImageResolver',
	version=__version__,
	author='Chris Brown',
	author_email='chris.brown@nwyc.com',
	packages=['imageresolver','imageresolver.abpy'],
	data_files=[(os.path.join( get_python_lib(),'imageresolver','data'),[ os.path.join('imageresolver','data','whitelist.txt') , os.path.join('imageresolver','data','blacklist.txt')])],
	scripts=['bin/resolveimg.py'],
	url='https://github.com/constituentvoice/ImageResolverPython',
	license='BSD',
	description="Find the most significant image in an article.",
	long_description=open('README.rst').read(),
	install_requires=[ "requests >= 1.0.0","beautifulsoup4" ],
	test_suite='tests'
)
