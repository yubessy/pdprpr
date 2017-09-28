from distutils.core import setup

setup(
    name='pdprpr',
    version='0.3.0',
    author='Shotaro Tanaka',
    author_email='yubessy0@gmail.com',
    packages=['pdprpr', 'pdprpr.series'],
    url='https://github.com/yubessy/pdprpr',
    license='LICENSE',
    description='Pdprpr preprocesses pandas objects (DataFrame, Series) for machine learning input.',
    long_description=open('README.md').read(),
    install_requires=[
        "attrs >= 17.1.0",
        "pandas >= 0.18.1",
    ],
)
