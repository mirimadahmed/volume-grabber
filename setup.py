from setuptools import setup, find_packages

setup(
    name="volume-grabber",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'python-dotenv==1.0.0',
    ]
) 