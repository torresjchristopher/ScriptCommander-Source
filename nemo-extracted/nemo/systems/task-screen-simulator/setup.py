"""
Setup configuration for Nemo Synthesis Engine.
Enables: pip install -e . or python setup.py install
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version
version_file = Path(__file__).parent / "VERSION"
version = version_file.read_text().strip() if version_file.exists() else "1.0.0"

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="nemo-synthesis-engine",
    version=version,
    author="Your Name",
    author_email="your.email@example.com",
    description="Nemo: AI-powered personal assistant via keyboard synthesis and screen analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_ORG/project-nemo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'click>=8.1.0',
        'rich>=13.0.0',
        'pyttsx3>=2.90',
        'google-cloud-texttospeech>=2.14.0',
        'pynput>=1.7.6',
        'psutil>=5.9.6',
    ],
    entry_points={
        'console_scripts': [
            'nemo=cli:cli',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['VERSION', '*.md', 'requirements.txt'],
    },
)
