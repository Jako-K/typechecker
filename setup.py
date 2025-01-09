from setuptools import setup, find_packages

setup(
    name="typechecker",
    version="0.0.1",
    description="A Python library for runtime type checking.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jakob",
    url="https://github.com/Jako-K/typechecker",
    packages=find_packages(),
    install_requires=["pytest"], 
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
