from setuptools import setup

setup(
    zip_safe=True,
    name='aria-rest',
    version='0.1',
    author='dewayne',
    author_email='dewayne@gigaspaces.com',
    packages=[
        'aria_rest'
    ],
    entry_points = {
      'console_scripts' : ['aria-rest=onap_aria_rest.rest:main']
    },
    license='LICENSE',
    description='Aria REST API for ONAP',
    install_requires=[
        'Flask==0.12.2'
    ]
)
