# coding: utf-8
from setuptools import setup, find_packages


setup(
    name='gomoku',
    version='1.0.0',
    description='An abstract strategy board game',

    url='http://gomoku.piatus.net/',
    author='piratus',
    author_email='piratus@gmail.com',
    license='WTFPL',

    packages=find_packages(),
    package_data={
        'gomoku': [
            'templates/*.html',
            'static/dist/*.*',
        ]
    },

    install_requires=[
        'funcy==1.5',
        'tornado==4.2',
    ]
)
