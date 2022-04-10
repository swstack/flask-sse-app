from distutils.core import setup
from setuptools import find_packages


def get_requirements():
    with open("requirements.txt", 'rb') as reqs:
        return list(map(lambda line: line.strip().decode('utf-8'), reqs.readlines()))


setup(
    name="flask-sse-app",
    version="0.0.1",
    description="Flask/SSE Toy Project",
    author="Stack, Stephen",
    author_email="sfstack7500@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements()
)
