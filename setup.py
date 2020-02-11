import setuptools
from os import path

# if you want a requirements.txt as well, use this code and specify install_requires=requirements
with open(path.join(path.dirname(path.realpath(__file__)), 'requirements.txt'), 'r') as f:
    requirements = [l.strip() for l in f if len(l) > 0 and not l.isspace()]

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
    package_data={'': ['*.yaml', '*.txt']},  # automatically include yaml/txt files

    # include other files such as html, css, etc
    include_package_data=True,  # read from MANIFEST.in
    zip_safe=True,

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Apache 2.0 License',
        'Operating System :: OS Independent',
    ],

    # for testing
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],

    # regular dependencies
    install_requires=requirements,
    # extra dependencies
    extras_require={
        'showcase': ['streamlit']
    }
)
