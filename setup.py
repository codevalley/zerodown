from setuptools import setup, find_packages
import os

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read the version from __init__.py
with open(os.path.join("zerodown", "__init__.py"), encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

setup(
    name="zerodown",
    version=version,
    description="Zero effort Markdown website generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zerodown Team",
    author_email="example@example.com",
    url="https://github.com/yourusername/zerodown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Jinja2>=3.0",
        "Markdown>=3.3",
        "python-frontmatter>=1.0",
        "PyYAML>=5.4",
    ],
    entry_points={
        "console_scripts": [
            "zerodown=zerodown.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.7",
)
