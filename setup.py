import setuptools
from os import path

setuptools.setup(
    name='phrasal',
    version='0.0.1',
    author='Lucy Linder',
    author_email='lucy.derlin@gmail.com',
    license='Apache License 2.0',
    description='Get meaningful text from HTML pages',
    url='',

    # install all packages found under src/
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src', exclude=['showcase']),
    #package_data={'': ['*.yaml', '*/*.yaml', '*.txt', '*/*.txt']},  # automatically include yaml/txt files

    # include other files such as html, css, etc
    include_package_data=True,  # read from MANIFEST.in
    zip_safe=True, # not safe if the library needs to read package data from os (path is different from a zip)

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Apache 2.0 License',
        'Operating System :: OS Independent',
    ],

    # for testing
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-check'],

    # regular dependencies
    install_requires=[
        'requests>=2.22,<2.23',
        'regex>=2020.1, <2020.2',
        'bs4',
        'justext==2.2.0',
        'ftfy>=5.6',
        'pyyaml>=5.3',
    ],
    # extra dependencies
    extras_require={
        'showcase': ['streamlit']
    }
)
