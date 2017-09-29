from distutils.core import setup

setup(
    name='pdprpr',
    version='0.6.1',
    author='Shotaro Tanaka',
    author_email='yubessy0@gmail.com',
    packages=['pdprpr', 'pdprpr.series'],
    url='https://github.com/yubessy/pdprpr',
    license='LICENSE',
    description=(
        'transform pandas objects (DataFrame / Series) into some form'
        ' suitable for machine learning input.'
    ),
    long_description=open('README.rst').read(),
    install_requires=[
        "attrs >= 17.1.0",
        "pandas >= 0.18.1",
    ],
)
