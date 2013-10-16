from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os

setup(
	name='ImageResolver',
	version='0.1.3',
	author='Chris Brown',
	author_email='chris.brown@nwyc.com',
	packages=['imageresolver','imageresolver.test','imageresolver.abpy'],
	data_files=[(os.path.join( get_python_lib(),'imageresolver','data'),[ os.path.join('imageresolver','data','whitelist.txt') , os.path.join('imageresolver','data','blacklist.txt')])],
	scripts=['bin/resolveimg.py'],
	url='https://github.com/chrisbrownnwyc/ImageResolverPython',
	license='BSD',
	description="Find the most significant image in an article.",
	long_description=open('README.txt').read(),
	install_requires=[ "requests >= 1.0.0","beautifulsoup4" ],
)
