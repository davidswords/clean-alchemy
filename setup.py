from setuptools import setup, find_packages

def read_requirements(file_name):
    with open(file_name) as f:
        return f.read().splitlines()

setup(
    name="clean-alchemy",
    version="0.1.13",
    packages=find_packages(exclude=["tests*", "build*"]),
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
    },
    author="David Swords",
    author_email="furuer_svette.0k@icloud.com",
    description="A framework for implementing Clean Architecture using SQLAlchemy for FastAPI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="https://github.com/davidswords/clean-alchemy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.3",
)