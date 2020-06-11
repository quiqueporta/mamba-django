from setuptools import setup

from mamba_django import __version__


setup(
    name='mamba-django',
    version=__version__,
    license='GPLv3',
    author='Quique Porta',
    author_email='quiqueporta@gmail.com',
    description='A Django test runner for mamba (the definitive test runner for Python).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/quiqueporta/mamba-django',
    download_url='https://github.com/quiqueporta/mamba-django/releases',
    keywords=['python', 'bdd', 'testing', 'tdd', 'django'],
    packages=['mamba_django'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
