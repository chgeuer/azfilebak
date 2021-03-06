from setuptools import setup

setup(
    name = 'azfilebak',
    version = '1.0-alpha1',
    packages = ['azfilebak'],
    description="A backup utility for file systems into Azure blob storage",
    author="Microsoft",
    author_email='chgeuer@microsoft.com',
    entry_points = {
        'console_scripts': [
            'azfilebak = azfilebak.__main__:main'
        ]
    },
    install_requires=[
        'pid>=2.2.0',
        'azure-storage-common>=1.3.0',
        'azure-storage-blob>=1.3.0',
        'msrestazure>=0.4.14',
        'psutil'
    ],
    tests_require=[
        'mock'
    ])
