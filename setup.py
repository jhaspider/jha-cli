from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jha",
    version="1.0.0",
    author="Amarjit Jha",
    description="JHA - Just Help Assistant. LLM-powered CLI command discovery.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhaspider/jha-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer==0.15.1",
        "openai==2.8.1",
        "pydantic==2.10.0",
        "python-dotenv==1.0.1",
        "click==8.1.7",
        "rich==13.9.4",
    ],
    entry_points={
        "console_scripts": [
            "jha=src.cli:main",
            "jhax=src.cli:explain",
        ],
    },
    include_package_data=True,
    keywords="cli llm openai command assistant",
)
