from setuptools import setup, find_packages

# Read the content of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read the contents of the requirements.txt file
requirements_path = this_directory / "requirements.txt"
with open(requirements_path, 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name='crew-as-code',
    version='0.1.8',
    author='Samuel Chung',
    author_email='samuelchung95@gmail.com',
    description='A simple package to manage your crew as code.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important to correctly render your README.md
    url='https://github.com/samchung95/Crew-as-code',  # URL to the project's repository
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
    # extras_require={
    #     'dev': [
    #         'check-manifest',
    #         'coverage',
    #         # Add other development dependencies here
    #     ],
    # },
    # entry_points={
    #     'console_scripts': [
    #         'your_command=your_module:main_function',
    #     ],
    # },
    include_package_data=True,
    # package_data={
    #     'your_package': ['data/*.dat'],
    # },
)
