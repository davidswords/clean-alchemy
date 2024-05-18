from setuptools import setup, find_packages

setup(
    name="clean-alchemy",
    version="0.1.10",
    packages=find_packages(where="src", exclude=["tests*", "build*"]),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "annotated-types==0.6.0",
        "black==24.4.2",
        "click==8.1.7",
        "exceptiongroup==1.2.1",
        "factory-boy==3.3.0",
        "Faker==25.0.1",
        "iniconfig==2.0.0",
        "mypy-extensions==1.0.0",
        "packaging==24.0",
        "pathspec==0.12.1",
        "platformdirs==4.2.1",
        "pluggy==1.5.0",
        "psycopg2==2.9.9",
        "pydantic==2.7.1",
        "pydantic_core==2.18.2",
        "pytest==8.2.0",
        "pytest-mock==3.14.0",
        "pytest-sugar==1.0.0",
        "python-dateutil==2.9.0.post0",
        "six==1.16.0",
        "SQLAlchemy==2.0.30",
        "termcolor==2.4.0",
        "tomli==2.0.1",
        "typing_extensions==4.11.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.2.0",
            "pytest-mock==3.14.0",
            "factory-boy==3.3.0",
            "pytest-sugar==1.0.0",
        ],
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
    python_requires=">=3.9.6",
)
