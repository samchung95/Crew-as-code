from setuptools import setup, find_packages

# Read the content of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='your_project_name',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your project',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important to correctly render your README.md
    url='https://github.com/yourusername/yourproject',  # URL to the project's repository
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'required_package1',
        'required_package2',
        # Add other dependencies here
    ],
    extras_require={
        'dev': [
            'check-manifest',
            'coverage',
            # Add other development dependencies here
        ],
    },
    entry_points={
        'console_scripts': [
            'your_command=your_module:main_function',
        ],
    },
    include_package_data=True,
    package_data={
        'your_package': ['data/*.dat'],
    },
)
