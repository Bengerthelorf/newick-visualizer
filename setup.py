from setuptools import setup, find_packages
import os

# 读取 _version.py 中的 __version__ 变量
version = {}
with open(os.path.join("newick_visualizer", "_version.py")) as fp:
    exec(fp.read(), version)

setup(
    name="newick-visualizer",
    version=version["__version__"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=8.0.0',
    ],
    entry_points={
        'console_scripts': [
            'newick-viz=newick_visualizer.cli.commands:main',
        ],
    },
    package_data={
        'newick_visualizer': [
            'templates/base.html',
            'templates/styles/*.css',
            'templates/scripts/*.js',
        ],
    },
    author="Zane Loeng",
    author_email="efd@live.com",
    description="A tool for visualizing Newick format phylogenetic trees",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Bengerthelorf/newick-visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)