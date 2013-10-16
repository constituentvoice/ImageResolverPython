from distutils.core import setup

setup(
	name='ImageResolver',
	version='0.1.0',
	author='Chris Brown',
	author_email='chris.brown@nwyc.com',
	packages=['imageresolver','imageresolver.test','imageresolver.abpy'],
	scripts=['bin/example.py'],
	url='https://github.com/chrisbrownnwyc/ImageResolverPython',
	license='LICENSE.txt',
	description="Find the most significant image in an article.",
	long_description=open('README.md').read(),
	install_requires=[ "requests >= 1.0.0","beautifulsoup4" ],
)
