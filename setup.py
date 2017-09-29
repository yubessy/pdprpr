from distutils.core import setup

NAME = 'pdprpr'
VERSION = '0.7.2'
LICENSE = 'LICENSE'

DESCRIPTION = 'PanDas PRePRocessor: Preprocess Pandas Objects for Machine Learning'
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()
URL = 'https://github.com/yubessy/pdprpr'

AUTHOR = 'Shotaro Tanaka'
AUTHOR_EMAIL = 'yubessy0@gmail.com'

PACKAGES = ['pdprpr', 'pdprpr.series']
INSTALL_REQUIRES = [
    'attrs >= 17.1.0',
    'pandas >= 0.18.1',
]

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
)
