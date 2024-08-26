from setuptools import setup, find_packages

setup(
    name="awarecache",
    version="1.5.11",
    packages=find_packages(include=["awarecache", "awarecache.*"]),
    install_requires=[],
    tests_require=["pytest"],
    author="Tobi Ayodeji",
    author_email="philayodeji07@gmail.com",
    description="A context-aware caching library with customizable policies and metrics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tobi2x/awarecache",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
