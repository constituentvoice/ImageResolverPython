from __future__ import absolute_import
from distutils.core import setup

# read the version directly instead of importing it
exec(open("imageresolver/version.py").read())

setup(
    name='ImageResolver',
    version=__version__,
    author='Chris Brown',
    author_email='chris.brown@nwyc.com',
    packages=['imageresolver', 'imageresolver.abpy', 'imageresolver.plugins'],
    package_data={'imageresolver': ['data/*.txt']},
    url='https://github.com/constituentvoice/ImageResolverPython',
    license='BSD',
    description="Find the most significant image in an article.",
    long_description=open('README.rst').read(),
    install_requires=["requests >= 1.0.0", "beautifulsoup4"],
    test_suite='tests'
)
